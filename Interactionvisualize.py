import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 設定：プレゼン用に見やすく
plt.rcParams.update({'font.size': 16})

# 図の準備 (アスペクト比を考慮して高さを少し増やす)
fig, ax = plt.subplots(figsize=(8, 5))

# アスペクト比を固定（これで円が楕円にならなくなる）
ax.set_aspect('equal')

# 1. 粒子の描画 (円)
# 左の粒子 (Particle 1)
p1 = patches.Circle((0.2, 0.5), 0.1, color='#3498db', ec='black', lw=2, zorder=10)
ax.add_patch(p1)

# 右の粒子 (Particle 2)
p2 = patches.Circle((0.8, 0.5), 0.1, color='#3498db', ec='black', lw=2, zorder=10)
ax.add_patch(p2)

# 2. 粒子ラベル (位置を少し調整)
ax.text(0.2, 0.3, 'Particle $i$', ha='center', va='top', fontsize=16)
ax.text(0.8, 0.3, 'Particle $j$', ha='center', va='top', fontsize=16)

# 3. 距離 r の表示
# 粒子の中心間に線を引く（点線）
ax.plot([0.2, 0.8], [0.5, 0.5], color='gray', linestyle='--', linewidth=1.5, zorder=1)
# "r" という文字と矢印 (位置を少し上に)
ax.annotate('', xy=(0.2, 0.7), xytext=(0.8, 0.7),
            arrowprops=dict(arrowstyle='<->', color='black', lw=1.5))
ax.text(0.5, 0.72, 'Distance $r$', ha='center', va='bottom', fontsize=16)

# 4. 力 F の表示 (引き合う力 = 引力)
# 矢印の始点を粒子から少し離す
# 左の粒子に働く力 (右向き)
ax.arrow(0.32, 0.5, 0.15, 0, head_width=0.05, head_length=0.05, fc='#e74c3c', ec='#e74c3c', width=0.015, zorder=5)
# 右の粒子に働く力 (左向き)
ax.arrow(0.68, 0.5, -0.15, 0, head_width=0.05, head_length=0.05, fc='#e74c3c', ec='#e74c3c', width=0.015, zorder=5)

# 力のラベル (位置を調整)
ax.text(0.4, 0.55, '$F_{ij}$', color='#e74c3c', fontsize=18, fontweight='bold', ha='center')
ax.text(0.6, 0.55, '$F_{ji}$', color='#e74c3c', fontsize=18, fontweight='bold', ha='center')

# 5. LJポテンシャルの数式 (位置を下に調整)
ax.text(0.5, 0.05, r'$V(r) = 4\epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^{6} \right]$',
        ha='center', va='center', fontsize=18, bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="gray", alpha=0.8))

# 軸を調整（余白を持たせる）
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.2, 0.9)
ax.axis('off')

plt.title('Lennard-Jones Interaction Model', fontsize=18, pad=20)
plt.tight_layout()

# 保存
plt.savefig('lj_schematic.png', dpi=300, bbox_inches='tight')
print("保存完了: lj_schematic.png")

plt.show()