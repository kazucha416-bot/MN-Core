# MN-CoreのLJフォースの誤差の散布図を作成する（単精度版）

import os
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
    
    plt.scatter(x_data, y_data, s=100, marker='o', c='red', edgecolors='none')
    
    # 画角設定 (中央に寄せるための広角設定)
    plt.xlim(1e-3, 1e7)
    plt.ylim(1e-8, 1e-5)

    plt.xscale('log')
    plt.yscale('log')
    
    plt.xlabel(r'$|F_{\mathrm{CPU}}|$', fontsize=16)
    plt.ylabel(r'$\delta$', fontsize=16)
    
    # ★変更点: タイトル削除
    # plt.title('MN-Core Accuracy', fontsize=16)
    
    plt.tick_params(labelsize=14)
    plt.grid(True, which="both", linestyle=':', alpha=0.6)
    # plt.legend(fontsize=14, loc='upper right')
    
    plt.tight_layout()
    # --- 保存先の変更 ---
    save_dir = r'/home/kazuki/thesis/images' # 指定された保存先ディレクトリ
    
    # もしディレクトリが存在しなければ作成する（念のため）
    os.makedirs(save_dir, exist_ok=True)
    
    # パスを結合して保存
    output_filename = 'Force_Error_Scatter_Float.pdf'
    output_path = os.path.join(save_dir, output_filename)
    
    plt.savefig(output_path)
    print(f"Graph saved: {output_path}")
    # plt.show()
else:
    print("No data found.")