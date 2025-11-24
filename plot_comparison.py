import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 設定 ---
file_A = 'lj_oscillator_1D.txt' # (CPU)
file_B = 'lj_oscillator_1D_float.txt'      # (MN-Core2) ★ここを変更しました

output_image = 'lj_comparison_final_fixed.png'

# ファイルAの列名
columns_A = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']
# ファイルBの列名
columns_B = ['TotalE_MNCORE']

# --- データ読み込み ---
try:
    data_A = pd.read_csv(
        file_A, 
        sep='\s+', 
        header=None, 
        names=columns_A, 
        comment='#'
    )
    print(f"'{file_A}' を読み込みました。 (全 {len(data_A)} 行)")

    data_B = pd.read_csv(
        file_B, 
        header=None, 
        names=columns_B
    )
    print(f"'{file_B}' を読み込みました。 (全 {len(data_B)} 行)")

    # --- グラフ作成 ---
    
    num_points = len(data_B) 
    
    time_axis = data_A['Time'].head(num_points)
    totalE_A = data_A['TotalE'].head(num_points)
    totalE_B = data_B['TotalE_MNCORE']

    # --- プロット準備 ---
    fig = plt.figure(figsize=(10, 6))
    
    # 左余白(left)を広げてY軸ラベルのスペースを確保 [left, bottom, width, height]
    ax = fig.add_axes([0.18, 0.13, 0.81, 0.86]) 

    # 1. CPU (点線、デフォルト青)
    ax.plot(time_axis, totalE_A, label='CPU', linestyle='--', linewidth=3.0)
    # 2. MN-Core2 (実線、デフォルトオレンジ)
    ax.plot(time_axis, totalE_B, label='MN-Core2', linewidth=3.0)
    
    # --- グラフの体裁 ---
    
    # 軸ラベル
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('Total Energy', fontsize=28)
    
    # 目盛りの数字サイズ
    ax.tick_params(axis='x', labelsize=22)
    ax.tick_params(axis='y', labelsize=18) # Y軸は少し小さくしてはみ出し防止
    
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # 凡例 (枠なし・特大)
    ax.legend(fontsize=18, loc='best', frameon=False)
    
    # --- ファイルに保存 ---
    plt.savefig(output_image)
    print(f"比較グラフを '{output_image}' として保存しました。")

except FileNotFoundError as e:
    print(f"エラー: {e.filename} が見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
