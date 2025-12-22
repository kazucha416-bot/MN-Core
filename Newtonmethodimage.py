import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def f(y, r):
    return y**(-2) - r

def df(y):
    return -2 * y**(-3)

def newton_step(y, r):
    # y_new = y * (1.5 - 0.5 * r * y * y) と同義ですが
    # 接線の作図のために f(y)/f'(y) の形式で計算します
    val = f(y, r)
    slope = df(y)
    return y - val / slope

def plot_newton_iterations(r, y0, iterations=3):
    # 設定
    y_target = 1.0 / np.sqrt(r)
    
    # プロット用のx軸範囲 (yの範囲)
    # グラフを見やすくするために範囲を調整
    y_vals = np.linspace(0.1, y_target * 1.8, 400)
    z_vals = f(y_vals, r) # z = f(y) = y^-2 - r

    plt.figure(figsize=(12, 8))
    
    # 1. 関数 f(y) の曲線をプロット
    plt.plot(y_vals, z_vals, label=r'$f(y) = y^{-2} - r$', color='blue', linewidth=2)
    plt.axhline(0, color='black', linewidth=1) # x軸 (z=0)

    # 現在の推定値
    current_y = y0
    
    # 色のリスト（反復ごとに色を変える）
    colors = ['red', 'green', 'orange']

    # 初期値 y0 の位置に点を打つ
    plt.scatter([current_y], [0], color=colors[0], marker='o', s=150, zorder=5, edgecolors='black', label='Estimates ($y_i$)')

    for i in range(iterations):
        # 現在の点 (y_n, f(y_n))
        val = f(current_y, r)
        slope = df(current_y)
        
        # 次の点 y_{n+1}
        next_y = newton_step(current_y, r)
        
        color = colors[i % len(colors)]
        
        # 垂直線: x軸から曲線上の点まで
        plt.plot([current_y, current_y], [0, val], linestyle='--', color=color, alpha=0.5)
        
        # 接線を描画: (y_n, f(y_n)) から (y_{n+1}, 0) まで
        # 接線の方程式: z - val = slope * (y - current_y)
        # 描画用に2点をつなぐだけでOK
        plt.plot([current_y, next_y], [val, 0], color=color, linewidth=2, 
                 label=f'Iteration {i+1} (Tangent at $y_{i}$)')
        
        # 点をプロット (曲線上の点)
        plt.scatter([current_y], [val], color=color, zorder=5)
        # ラベルのフォントサイズを拡大 (16 -> 24)
        plt.text(current_y, val + (1 if val > 0 else -1), f'$y_{i}$', 
                 color=color, fontsize=24, verticalalignment='bottom') 
        
        # 次の推定値の位置にマーク（x軸上）
        # マーカーを目立つ大きな円に変更
        plt.scatter([next_y], [0], color=color, marker='o', s=150, zorder=5, edgecolors='black')
        
        # x軸下のラベル表示(y_{i+1})を削除しました

        # 更新
        print(f"Iter {i+1}: y_{i} = {current_y:.5f} -> y_{i+1} = {next_y:.5f}")
        current_y = next_y

    # 真値の線
    plt.axvline(y_target, color='gray', linestyle=':', label=f'True value')

    # グラフの体裁（フォントサイズを全体的に拡大）
    plt.xlabel('$y$ (Estimate)', fontsize=18)
    plt.ylabel('$f(y)$', fontsize=18)
    
    # 軸目盛りの文字サイズも大きく
    plt.tick_params(axis='both', which='major', labelsize=14)
    
    plt.ylim(-r*1.5, f(y0, r)*1.2) # y0の開始点が見えるようにY軸調整
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right', fontsize=14)
    
    plt.tight_layout()
    # --- 保存処理 ---
    # 保存先のディレクトリとファイル名
    save_dir = r'/home/kazuki/thesis/images' 
    filename = 'newton_raphson_3iterations.pdf'  # 画質最強のPDFに変更しておきました！（PNGが良ければ.pngに戻してね）
    
    # パスを結合
    save_path = os.path.join(save_dir, filename)

    # ディレクトリが存在しない場合に備えて、なければ作る（念のため）
    os.makedirs(save_dir, exist_ok=True)

    # 保存実行
    plt.savefig(save_path, dpi=300)
    print(f"Graph saved as {save_path}")

    # plt.show() # 確認したいときはここを外す

# 実行: r=1.3, 初期値 y0=0.4 でシミュレーション
# 目標値は 1/sqrt(1.3) ≈ 0.877 です
plot_newton_iterations(r=1.3, y0=0.4, iterations=3)