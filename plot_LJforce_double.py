import re
import struct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os  # ディレクトリ操作用にインポート

def parse_dump_file_double_hex(filename):
    """
    ダンプファイルを解析して r と Force のペアを抽出する (倍精度対応版)
    16進数表記 (例: 0x3fe0000000000000) を読み込みます。
    """
    r_values = {}
    f_values = {}

    # 正規表現: インデックスと、16桁の16進数 (64bit) を抽出
    pattern_idx = re.compile(r",(\d+)\):")
    pattern_hex = re.compile(r"\(0x([0-9a-fA-F]{16})\)")

    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                
                # インデックス取得
                m_idx = pattern_idx.search(line)
                if not m_idx: continue
                idx = int(m_idx.group(1))

                # Hex値取得 (16桁)
                m_hex = pattern_hex.search(line)
                if not m_hex: continue
                hex_str = m_hex.group(1)

                # Hex -> Double変換 (Big-endian double precision)
                try:
                    val = struct.unpack('>d', bytes.fromhex(hex_str))[0]
                except ValueError: continue

                if "DEBUG-LM0" in line:
                    r_values[idx] = val
                elif "DEBUG-LM1" in line:
                    f_values[idx] = val

        # データフレーム化
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
filename = 'LJ_force_double.dmp' # ファイル名を指定
df = parse_dump_file_double_hex(filename)

if not df.empty:
    # 真値計算
    df['F_cpu'] = df['r'].apply(calculate_cpu_force_double)
    
    # プロットデータ作成
    x_data = np.abs(df['F_cpu'])
    
    # 相対誤差計算 (ゼロ除算防止に微小値を足す)
    epsilon = 1e-15
    y_data = np.abs(df['F_mn'] - df['F_cpu']) / (x_data + epsilon)

    # --- プロット設定 ---
    plt.figure(figsize=(10, 8))
    
    # マーカー: 青い丸 ('o')
    plt.scatter(x_data, y_data, s=40, marker='o', c='blue', edgecolors='none')
    
    # --- 画角の調整 (倍精度用に変更) ---
    plt.xlim(1e-5, 1e10)
    plt.ylim(1e-18, 1e-10)

    plt.xscale('log')
    plt.yscale('log')
    
    plt.xlabel(r'Absolute force of CPU $|F_{\mathrm{CPU}}|$', fontsize=16)
    plt.ylabel(r'Relative error $|F_{\mathrm{MN-Core 2}} - F_{\mathrm{CPU}}|  /  |F_{\mathrm{CPU}}|$', fontsize=16)
    
    plt.tick_params(labelsize=14)
    plt.grid(True, which="both", linestyle=':', alpha=0.6)
    # plt.legend(fontsize=14, loc='upper right') # 不要な凡例はコメントアウト済み
    
    plt.tight_layout()
    
    # --- 保存先の変更 ---
    save_dir = r'/home/kazuki/thesis/images' # 指定された保存先ディレクトリ
    
    # もしディレクトリが存在しなければ作成する（念のため）
    os.makedirs(save_dir, exist_ok=True)
    
    # パスを結合して保存
    output_filename = 'Force_Error_Scatter_Double.pdf'
    output_path = os.path.join(save_dir, output_filename)
    
    plt.savefig(output_path)
    print(f"Graph saved: {output_path}")
    
    # plt.show()
else:
    print("No data found.")