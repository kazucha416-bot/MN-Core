import numpy as np
import matplotlib.pyplot as plt
import struct
import os

def main():
    # --- 設定 ---
    output_filename = 'lj_single_axis_verification.pdf'
    r_mncore = np.linspace(1.0, 2.0, 11) # 1.0 ~ 2.0

    # --- データ定義 (Hex) ---
    # Potential (Pe) Data
    pe_hex_data = [
        "0x3d08000000000000",
        "0xbfef77c97fbb1dc6",
        "0xbfec82c9a2814c2a",
        "0xbfe506485610caa2",
        "0xbfdd7be500247fa1",
        "0xbfd480650f08dd2a",
        "0xbfccb2d6b5e0000a",
        "0xbfc4553cf183fe9c",
        "0xbfbd38bdceade1cd",
        "0xbfb54da72778a1e3",
        "0xbfaf7ffffffffff4"
    ]

    # Force (F) Data
    f_hex_data = [
        "0x403800000000003c",
        "0x3ff968d6b6238fa2",
        "0xc001b18c476d084b",
        "0xc001eb7a98f131dc",
        "0xbffac07fd22899e8",
        "0xbff287493d52b18d",
        "0xbfe9331a9504000b",
        "0xbfe12a5adf03e9ce",
        "0xbfd79d1d108d832e",
        "0xbfd07402b5a283fa",
        "0xbfc73ffffffffff5" # 修正済み
    ]

    # --- 関数定義 ---
    
    def hex_to_double(hex_str):
        # 0x, カンマ, 空白などを除去
        s = hex_str.strip().replace('0x', '').replace(',', '')
        # 0埋め (念のため)
        s = s.zfill(16)
        try:
            return struct.unpack('>d', bytes.fromhex(s))[0]
        except ValueError:
            return None

    def lj_potential_exact(r):
        r6_inv = (1.0 / r) ** 6
        return 4.0 * (r6_inv**2 - r6_inv)

    def lj_force_exact(r):
        r_inv = 1.0 / r
        r7_inv = r_inv ** 7
        r13_inv = r_inv ** 13
        return 48.0 * r13_inv - 24.0 * r7_inv

    # --- データ変換 ---
    pe_mncore = np.array([hex_to_double(h) for h in pe_hex_data])
    f_mncore  = np.array([hex_to_double(h) for h in f_hex_data])

    # 厳密解カーブ用
    r_exact = np.linspace(0.95, 2.05, 300)
    pe_exact = lj_potential_exact(r_exact)
    f_exact = lj_force_exact(r_exact)

    # --- プロット処理 ---
    plt.rcParams.update({'font.size': 18})
    plt.figure(figsize=(10, 8)) # 少し縦長にして見やすく

    # 基準線 (y=0)
    plt.axhline(0, color='gray', linestyle='-', linewidth=1.0, alpha=0.8)

    # === プロット ===
    
    # 1. Force (力) - 青色
    plt.plot(r_exact, f_exact, label='Exact Force', color='tab:blue', linestyle='-', linewidth=2, alpha=0.6)
    plt.scatter(r_mncore, f_mncore, label='MN-Core Force', color='tab:blue', marker='^', s=100, edgecolors='black', zorder=5)

    # 2. Potential (ポテンシャル) - 赤色
    plt.plot(r_exact, pe_exact, label='Exact Potential', color='tab:red', linestyle='--', linewidth=2, alpha=0.8)
    plt.scatter(r_mncore, pe_mncore, label='MN-Core Potential', color='tab:red', marker='o', s=100, edgecolors='black', zorder=5)

    # === レイアウト調整 ===
    plt.xlabel('Distance r', fontsize=22)
    plt.ylabel('Potential / Force (Dimensionless)', fontsize=22)
    
    plt.xlim(0.95, 2.05)
    
    # Y軸範囲の自動調整 (最大値・最小値からマージンをとる)
    all_vals = np.concatenate([pe_exact, f_exact])
    y_min, y_max = min(all_vals), max(all_vals)
    margin = (y_max - y_min) * 0.1
    plt.ylim(y_min - margin, y_max + margin)

    plt.grid(True, linestyle='--', alpha=0.5)
    
    # 凡例
    plt.legend(loc='upper right', frameon=False, fontsize=16)

    # 保存
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    main()