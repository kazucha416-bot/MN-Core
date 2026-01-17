import re
import struct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def parse_dump_file_hex(filename):
    """ダンプファイルを解析して r と Force のペアを16進数から厳密に抽出する"""
    r_values = {}
    f_values = {}

    pattern_idx = re.compile(r",(\d+)\):")
    pattern_hex = re.compile(r"\(0x([0-9a-fA-F]+), 0x[0-9a-fA-F]+\)")

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                m_idx = pattern_idx.search(line)
                if not m_idx: continue
                idx = int(m_idx.group(1))

                m_hex = pattern_hex.search(line)
                if not m_hex: continue
                hex_str = m_hex.group(1)

                try:
                    val = struct.unpack('>f', bytes.fromhex(hex_str))[0]
                except ValueError: continue

                if "DEBUG-LM0" in line:
                    r_values[idx] = val
                elif "DEBUG-LM1" in line:
                    f_values[idx] = val

        data_list = []
        sorted_indices = sorted(r_values.keys())
        for idx in sorted_indices:
            if idx in f_values:
                data_list.append({'r': r_values[idx], 'F_mn': f_values[idx]})
        
        return pd.DataFrame(data_list)
                
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return pd.DataFrame()

def calculate_cpu_force_double(r):
    """CPU (Double Precision) で真値を計算"""
    r7 = r**7
    r13 = r**13
    return 48.0 / r13 - 24.0 / r7

# --- メイン処理 ---
filename = 'generated_kernel.dmp'
df = parse_dump_file_hex(filename)

if not df.empty:
    # 真値計算
    df['F_cpu'] = df['r'].apply(calculate_cpu_force_double)
    
    # プロットデータ作成
    x_data = np.abs(df['F_cpu'])
    epsilon = 1e-15
    y_data = np.abs(df['F_mn'] - df['F_cpu']) / (x_data + epsilon)

    # --- プロット設定 ---
    plt.figure(figsize=(10, 8))
    
    # ★変更点: マーカーを星型(*)、色を青(blue)、塗りつぶしあり
    plt.scatter(x_data, y_data, s=60, marker='o', c='blue', edgecolors='none', label='MN-Core (Single) Error')
    
    # ★変更点: 赤線を削除 (倍精度のガイドラインだけ残す場合はこちら)
    # plt.axhline(1.19e-7, color='red', linestyle='--', linewidth=1.5, label=r'Single Precision $\epsilon$') 
    plt.axhline(1e-15, color='gray', linestyle=':', linewidth=1, label=r'Double Precision $\epsilon \approx 10^{-15}$')

    # 画角設定 (中央に寄せるための広角設定)
    plt.xlim(1e-5, 1e10)
    plt.ylim(1e-11, 1e-3)

    plt.xscale('log')
    plt.yscale('log')
    
    plt.xlabel(r'Force Magnitude $|F_{\mathrm{CPU}}|$', fontsize=16)
    plt.ylabel(r'Relative Error $|F_{\mathrm{MN}} - F_{\mathrm{CPU}}| / |F_{\mathrm{CPU}}|$', fontsize=16)
    
    # ★変更点: タイトル削除
    # plt.title('MN-Core Accuracy', fontsize=16)
    
    plt.tick_params(labelsize=14)
    plt.grid(True, which="both", linestyle=':', alpha=0.6)
    plt.legend(fontsize=14, loc='upper right')
    
    plt.tight_layout()
    output_file = 'Force_Error_Scatter_Final.pdf'
    plt.savefig(output_file)
    print(f"Graph saved: {output_file}")
    
    # plt.show()
else:
    print("No data found.")