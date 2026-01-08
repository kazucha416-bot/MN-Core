import numpy as np
import matplotlib.pyplot as plt
import os
# 設定：フォントサイズなどをスライド用に大きくする
plt.rcParams.update({'font.size': 14})

# ==========================================
# Harmonic Oscillator / Spring (線形)
# ==========================================

def spring_potential(x, k=1.0):
    """ばねのポテンシャル V(x) = 1/2 k x^2"""
    return 0.5 * k * x**2

def spring_force(x, k=1.0):
    """ばねの力 F(x) = -kx (線形)"""
    return -k * x

# 変位xの範囲 (平衡点0を中心に)
x = np.linspace(-2.0, 2.0, 500)
V_spring = spring_potential(x)
F_spring = spring_force(x)

# グラフ作成 (Spring)
plt.figure(figsize=(8, 6))

# ポテンシャルカーブ（青の実線）
plt.plot(x, V_spring, label='Potential', color='blue', linewidth=3)

# 力のカーブ（赤の点線：視認性を考慮して破線'--'にしています）
plt.plot(x, F_spring, label='Force', color='red', linestyle='--', linewidth=2)

# 軸の描画
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1, linestyle=':') # 平衡点

# ラベル設定（横軸ラベルをDistanceに変更）
plt.xlabel('Distance', fontsize=16)
plt.ylabel('Energy / Force', fontsize=16)

# グリッドと凡例
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=14)

# タイトルは無し
# plt.title(...) 

plt.tight_layout()

# PDFで保存
output_dir = '/home/kazuki/thesis/images/'
output_file = output_dir + 'spring_plot.pdf'
output_path = os.path.join(output_dir, output_file)
plt.savefig(output_path, dpi=300)
print(f"保存完了: {output_path}")

# plt.show()