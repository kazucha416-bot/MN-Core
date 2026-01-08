import numpy as np
import matplotlib.pyplot as plt

# 設定：フォントサイズなどを大きく
plt.rcParams.update({'font.size': 14})

def main():
    # --- パラメータ設定 ---
    epsilon = 1.0
    sigma = 1.0
    
    # クーロン力の係数 (q_coeff = k * q1 * q2)
    # 負の値 = 引力 (Attractive)
    q_coeff = -2.0 

    # 距離rの範囲
    r = np.linspace(0.8, 3.5, 500)

    # --- 1. Lennard-Jones Potential ---
    v_lj = 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)

    # --- 2. Coulomb Potential ---
    v_coul = q_coeff / r

    # --- 3. Total Potential ---
    v_total = v_lj + v_coul

    # --- プロット作成 ---
    plt.figure(figsize=(10, 6))

    # LJ (青・破線)
    plt.plot(r, v_lj, label='Lennard-Jones (LJ)', 
             color='blue', linestyle='--', linewidth=2, alpha=0.7)

    # Coulomb (緑・破線)
    plt.plot(r, v_coul, label=f'Coulomb (Attr: {q_coeff})', 
             color='green', linestyle='--', linewidth=2, alpha=0.7)

    # Total (赤・実線・太め)
    plt.plot(r, v_total, label='Total (LJ + Coulomb)', 
             color='red', linewidth=3)

    # 装飾
    plt.axhline(0, color='black', linewidth=1)
    plt.xlabel('Distance $r / \sigma$', fontsize=16)
    plt.ylabel('Potential Energy $V(r) / \epsilon$', fontsize=16)
    
    # 見やすいようにY軸の範囲を制限
    plt.ylim(-5.0, 3.0)
    plt.xlim(0.8, 3.5)
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12, loc='upper right')

    plt.tight_layout()

    # --- 保存処理 ---
    # カレントディレクトリに直接保存
    output_filename = 'lj_coulomb_potential_compare.pdf'
    
    plt.savefig(output_filename, dpi=300)
    print(f"グラフを保存しました: {output_filename}")

    # plt.show()

if __name__ == "__main__":
    main()