# 1次元LJばね問題におけるMN-Core2とCPU（単精度版）のエネルギー比較グラフを作成するスクリプト
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct
import numpy as np
import os
import sys

def hex_to_float(hex_str):
    """
    16進数文字列を単精度浮動小数点数に変換
    エラー対策：改行やスペースを除去し、8文字（4バイト）であることを確認
    """
    try:
        s = hex_str.strip().replace('0x', '')
        # 文字列が空、または長さがおかしい場合はNoneを返す
        if len(s) != 8:
            return None
        # big-endian float (>f)
        return struct.unpack('>f', bytes.fromhex(s))[0]
    except Exception:
        return None

def main():
    # ==========================================
    # 設定エリア
    # ==========================================
    mn_file = '1227baneljfloat_result.txt'
    cpu_file = 'lj_oscillator_1D_float.txt'
    
    # 保存先ディレクトリ（卒論用フォルダ）
    save_dir = r'/home/kazuki/thesis/images'
    output_filename = 'MNCore2_vs_CPU_LJ_Energy_Single_Analysis.pdf'
    
    # フルパスの生成
    output_path = os.path.join(save_dir, output_filename)
    # ==========================================

    # --- 1. 保存先ディレクトリの確認 ---
    if not os.path.exists(save_dir):
        try:
            os.makedirs(save_dir)
            print(f"ディレクトリを作成しました: {save_dir}")
        except OSError as e:
            print(f"⚠️ ディレクトリ作成エラー: {e}")
            return

    # --- 2. MN-Coreデータの読み込み ---
    print(f"Reading MN-Core file: {mn_file}")
    mn_energies = []
    
    if os.path.exists(mn_file):
        with open(mn_file, 'r') as f:
            for line in f:
                val = hex_to_float(line)
                if val is not None:
                    mn_energies.append(val)
    else:
        print(f"【エラー】ファイルが見つかりません: {mn_file}")
        return

    # --- 3. CPUデータの読み込み ---
    print(f"Reading CPU file: {cpu_file}")
    cpu_time = []
    cpu_energies = []
    
    if os.path.exists(cpu_file):
        try:
            # ★修正1: delim_whitespace警告対策 -> sep=r'\s+' を使用
            df = pd.read_csv(cpu_file, sep=r'\s+', comment='#', header=None)
            
            # データ列の取得 (0列目:Time, 4列目:TotalEnergy と仮定)
            cpu_time_full = df[0].values
            cpu_total_e_full = df[4].values 
            
            # 間引き処理 (MN-Coreデータと刻みを合わせるため 10ステップごとに抽出)
            step = 10
            cpu_time = cpu_time_full[::step]
            cpu_energies = cpu_total_e_full[::step]
            
        except Exception as e:
            print(f"【エラー】CPUデータ読み込み失敗: {e}")
            return
    else:
        print(f"【エラー】ファイルが見つかりません: {cpu_file}")
        return

    # --- 4. データ整合性チェック ---
    if len(mn_energies) == 0:
        print("【エラー】MN-Coreデータが読み込めませんでした（0件）。")
        return
    if len(cpu_energies) == 0:
        print("【エラー】CPUデータが読み込めませんでした（0件）。")
        return

    # 配列長を揃える（短い方に合わせる）
    min_len = min(len(mn_energies), len(cpu_energies))
    print(f"データ点数: MN-Core={len(mn_energies)}, CPU={len(cpu_energies)} -> 使用={min_len}")

    mn_energies = np.array(mn_energies[:min_len])
    cpu_energies = np.array(cpu_energies[:min_len])
    cpu_time = cpu_time[:min_len]

    # --- 5. 誤差解析 ---
    abs_errors = np.abs(mn_energies - cpu_energies)
    max_error = np.max(abs_errors)
    mean_error = np.mean(abs_errors)
    
    print("-" * 60)
    print("Error Analysis (MN-Core 2 vs CPU [Single Precision])")
    print("-" * 60)
    print(f"Max Error  : {max_error:.6e}")
    print(f"Mean Error : {mean_error:.6e}")
    print("-" * 60)

    # --- 6. プロット作成 ---
    plt.rcParams.update({'font.size': 14})
    plt.figure(figsize=(10, 6))
    
    ax = plt.gca()

    # CPU (Reference) - 黒実線
    ax.plot(cpu_time, cpu_energies, label='CPU (Single)', 
             color='black', linewidth=2.0, alpha=0.8)

    # MN-Core - 赤破線
    ax.plot(cpu_time, mn_energies, label='MN-Core 2 (Single)', 
             color='red', linestyle='--', linewidth=2.0, alpha=0.9)

    # ラベル設定
    # ★修正2: \m 警告対策 -> raw string (r'') を使用
    ax.set_xlabel('Time [-]', fontsize=16)
    ax.set_ylabel(r'$E_{\mathrm{total}}$ [-]', fontsize=16)
    
    ax.legend(fontsize=16, loc='upper right', frameon=False)
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Y軸の数値フォーマット（オフセット表示を無効化する場合）
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)
    
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_path, dpi=300)
    print(f"グラフを保存しました: {output_path}")

if __name__ == "__main__":
    main()