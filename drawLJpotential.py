import numpy as np
import matplotlib.pyplot as plt

# 設定：フォントサイズなどをスライド用に大きくする
plt.rcParams.update({'font.size': 14})

# ==========================================
# 1. Lennard-Jones Potential (非線形)
# ==========================================

def lj_potential(r, epsilon=1.0, sigma=1.0):
    """レナード・ジョーンズ・ポテンシャル V(r)"""
    return 4 * epsilon * ((sigma / r)**12 - (sigma / r)**6)

def lj_force(r, epsilon=1.0, sigma=1.0):
    """LJの力 F(r) = -dV/dr (非線形)"""
    term12 = (sigma / r)**12
    term6 = (sigma / r)**6
    return 24 * epsilon * (2 * term12 - term6) / r

# 距離rの範囲
r = np.linspace(0.85, 3.0, 500)
V_lj = lj_potential(r)
F_lj = lj_force(r)

# グラフ作成 (LJ)
plt.figure(figsize=(8, 6))
plt.plot(r, V_lj, label='Potential $V(r) \propto r^{-12} - r^{-6}$', color='blue', linewidth=3)
plt.plot(r, F_lj, label='Force $F(r)$ (Non-linear)', color='red', linestyle='--', linewidth=2)
plt.axhline(0, color='black', linewidth=1)
plt.xlabel('Distance $r / \sigma$', fontsize=16)
plt.ylabel('Energy / Force', fontsize=16)
plt.ylim(-1.5, 3.0)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=14)
plt.title('Lennard-Jones (Non-linear)', fontsize=18)
plt.tight_layout()
plt.savefig('lj_plot.png', dpi=300)
print("保存完了: lj_plot.png (非線形の例)")
# plt.show() # 連続して表示するために一旦コメントアウト


# ==========================================
# 2. Harmonic Oscillator / Spring (線形)
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
# ポテンシャルは放物線
plt.plot(x, V_spring, label='Potential $V(x) = \\frac{1}{2}kx^2$', color='green', linewidth=3)
# 力は直線（これが「線形」の由来！）
plt.plot(x, F_spring, label='Force $F(x) = -kx$ (Linear)', color='orange', linestyle='--', linewidth=2)

plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1, linestyle=':') # 平衡点
plt.xlabel('Displacement $x$', fontsize=16)
plt.ylabel('Energy / Force', fontsize=16)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=14)
plt.title('Harmonic Oscillator (Linear)', fontsize=18)
plt.tight_layout()
plt.savefig('spring_plot.png', dpi=300)
print("保存完了: spring_plot.png (線形の例)")

plt.show()