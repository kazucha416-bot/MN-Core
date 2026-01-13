import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot_snapshot_clean(positions, lattice_constant=2.0, save_path="snapshot_angle.pdf", 
                        elev=30, azim=60):
    """
    視点変更機能付き：格子枠（実線）と粒子のみをPDF保存します。
    
    Args:
        elev (float): 仰角（上下の角度）。90で真上、0で真横。
        azim (float): 方位角（左右の回転）。
    """
    pos_np = np.array(positions)
    
    if pos_np.shape != (4, 3):
        print("Error: Positions must be a list/array of shape (4, 3).")
        return

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # --- 1. 粒子をプロット ---
    ax.scatter(pos_np[:, 0], pos_np[:, 1], pos_np[:, 2], 
               color='red', s=200, label='Particles', alpha=0.9, edgecolors='black')

    # --- 2. 格子枠を描画 (実線) ---
    L = lattice_constant
    corners = np.array([
        [0, 0, 0], [L, 0, 0], [L, L, 0], [0, L, 0],
        [0, 0, L], [L, 0, L], [L, L, L], [0, L, L]
    ])
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7)
    ]
    for start, end in edges:
        ax.plot3D(*zip(corners[start], corners[end]), 
                  color='black', linestyle='-', linewidth=1.5, alpha=1.0)

    # --- 3. グラフ設定 ---
    ax.set_axis_off() # 軸を消す

    # 範囲固定
    all_coords = np.vstack([pos_np, corners])
    min_val = all_coords.min() - 0.5
    max_val = all_coords.max() + 0.5
    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_zlim(min_val, max_val)
    ax.set_box_aspect((1, 1, 1))
    
    # ★視点の変更 (ここをいじります)
    # elev: 上下の角度 (0=真横, 90=真上)
    # azim: 左右の回転
    ax.view_init(elev=elev, azim=azim)
    
    plt.tight_layout()
    plt.savefig(save_path, format='pdf', bbox_inches='tight', pad_inches=0.1)
    print(f"保存しました (elev={elev}, azim={azim}): {save_path}")
    plt.close()

if __name__ == "__main__":
    my_positions = [
        [0.266,  -0.275,  -0.302],
        [-0.413,  1.363, 0.864],
        [1.014, 0.933,  0.366],
        [1.132, -0.022,  1.072]
    ]
    
    # 実行例: いろいろな角度で出力してみる
    
    # 1. デフォルト (少し斜めから)
    plot_snapshot_clean(my_positions, save_path="snapshot_angle_1.pdf", elev=30, azim=60)
    
    # 2. 真上から (XY平面配置を見る)
    plot_snapshot_clean(my_positions, save_path="snapshot_angle_top.pdf", elev=90, azim=-90)
    
    # 3. ほぼ真横から (XZ平面配置を見る)
    plot_snapshot_clean(my_positions, save_path="snapshot_angle_side.pdf", elev=10, azim=0)