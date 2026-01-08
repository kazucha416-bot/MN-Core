import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct
import numpy as np
import os

def hex_to_float(hex_str):
    """16進数文字列を単精度浮動小数点数に変換"""
    s = hex_str.strip().replace('0x', '')
    try:
        # big-endian float (>f)
        return struct.unpack('>f', bytes.fromhex(s))[0]
    except Exception as e:
        return None

def main():
    # --- 設定 ---
    mn_file = '1227baneljfloat_result.txt'
    cpu_file = 'lj_oscillator_1D_float.txt'
    output_filename = 'MNCore2_vs_CPU_LJ_Energy_Single_Analysis.pdf'

    # --- 1. MN-Coreデータの読み込み ---
    mn_energies = []
    if os.path.exists(mn_file):
        with open(mn_file, 'r') as f:
            for line in f:
                if line.strip():
                    val = hex_to_float(line)
                    if val is not None:
                        mn_energies.append(val)
    else:
        print(f"エラー: {mn_file} が見つかりません。")
        return

    # --- 2. CPUデータの読み込み ---
    cpu_time = []
    cpu_energies = []
    if os.path.exists(cpu_file):
        try:
            # ヘッダー(#)を無視して空白区切りで読み込み
            df = pd.read_csv(cpu_file, delim_whitespace=True, comment='#', header=None)
            
            cpu_time_full = df[0].values
            cpu_total_e_full = df[4].values # 5列目がTotal Energy
            
            # --- 間引き処理 ---
            # データ数を合わせるため 10ステップごとに抽出
            step = 10
            cpu_time = cpu_time_full[::step]
            cpu_energies = cpu_total_e_full[::step]
            
        except Exception as e:
            print(f"CPUデータ読み込みエラー: {e}")
            return
    else:
        print(f"エラー: {cpu_file} が見つかりません。")
        return

    # --- 3. データ点数の調整 ---
    min_len = min(len(mn_energies), len(cpu_energies))
    mn_energies = np.array(mn_energies[:min_len])
    cpu_energies = np.array(cpu_energies[:min_len])
    cpu_time = cpu_time[:min_len]
    
    print(f"比較データ点数: {min_len}")

    # --- 4. 誤差解析 (ここを追加) ---
    abs_errors = np.abs(mn_energies - cpu_energies)
    
    max_error = np.max(abs_errors)
    min_error = np.min(abs_errors)
    mean_error = np.mean(abs_errors)
    
    print("-" * 60)
    print("Error Analysis (MN-Core 2 vs CPU [Single Precision])")
    print("-" * 60)
    print(f"Absolute Error Range : {min_error:.6e} to {max_error:.6e}")
    print(f"Mean Absolute Error  : {mean_error:.6e}")
    print("-" * 60)

    # --- 5. プロット作成 ---
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(10, 6))
    
    ax = plt.gca()

    # CPU (Reference) - 黒実線
    ax.plot(cpu_time, cpu_energies, label='CPU (Single Precision)', 
             color='black', linewidth=2.0, alpha=0.8)

    # MN-Core - 赤破線
    ax.plot(cpu_time, mn_energies, label='MN-Core 2 (Single Precision)', 
             color='red', linestyle='--', linewidth=2.0, alpha=0.9)

    # ラベル設定
    ax.set_xlabel('Time', fontsize=16)
    ax.set_ylabel('Total Energy', fontsize=16)
    
    # 凡例表示
    ax.legend(fontsize=14)
    
    # グリッド表示
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Y軸のオフセット無効化
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)
    
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_filename, dpi=300)
    print(f"グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    main()