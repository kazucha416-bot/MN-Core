import numpy as np
import matplotlib.pyplot as plt

# --- LJポテンシャルの定義 ---
def lennard_jones_potential(r, epsilon=1.0, sigma=1.0):
    """
    レナード・ジョーンズ・ポテンシャルを計算する関数
    V(r) = 4 * epsilon * [ (sigma/r)^12 - (sigma/r)^6 ]
    """
    # rが0に近すぎると発散するので、小さな値でクリップするか、範囲を制限する
    # ここでは描画範囲で制御します
    term = (sigma / r)**6
    return 4 * epsilon * (term**2 - term)

# --- データ生成 ---
# rの範囲を設定 (sigma=1として、少し手前から遠くまで)
r = np.linspace(0.85, 3.0, 500)
V = lennard_jones_potential(r)

# --- グラフの描画設定 ---
fig, ax = plt.subplots(figsize=(8, 6))

# プロット (線を太く、色をわかりやすく)
ax.plot(r, V, linewidth=4.0, color='blue', label='LJ Potential')

# V=0 の基準線を追加
ax.axhline(0, color='gray', linestyle='--', linewidth=2.0)

# --- 見た目の調整 ---

# 1. 軸の目盛り数値を消す
ax.set_xticks([])
ax.set_yticks([])

# 2. 枠線（スパイン）を太くする
spine_width = 3.0
for spine in ax.spines.values():
    spine.set_linewidth(spine_width)

# 3. 軸ラベルを追加（大きく、わかりやすく）
# 数値がない代わりに、何を表す軸かを明確にします
ax.set_xlabel(r'Distance $r$', fontsize=20, labelpad=10)
ax.set_ylabel(r'Potential Energy $V(r)$', fontsize=20, labelpad=10)

# グラフの表示範囲を調整（見やすい部分にフォーカス）
ax.set_ylim(-1.5, 2.0)
ax.set_xlim(0.8, 3.0)

# レイアウト調整
plt.tight_layout()

# --- 保存 ---
output_filename = 'lj_potential.png'
plt.savefig(output_filename, dpi=300)
print(f"グラフを {output_filename} に保存しました。")

# (確認用)
# plt.show()