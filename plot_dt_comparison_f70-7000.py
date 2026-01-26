# シンプレクティックEuler法の異なる時間刻み幅によるエネルギー保存性の比較グラフを作成するスクリプト
# ファイル名: plot_dt_comparison_f70-7000.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os  # パス操作用

# --- 設定 ---
files_config = [
    # { 'filename': 'ファイル名', 'dt': 時間刻み幅, 'label': '凡例ラベル' }
    {'filename': 'resultnew_f70.txt',   'dt': 0.1,   'label': 'dt=0.1 s'},
    {'filename': 'result_f700.txt',     'dt': 0.01,  'label': 'dt=0.01 s'},
    {'filename': 'result_f7000.txt',    'dt': 0.001, 'label': 'dt=0.001 s'},
]

# 保存先の設定
save_dir = r'/home/kazuki/thesis/images'
output_filename = 'Euler_Differentsteps.pdf'

# 保存先のディレクトリが存在しない場合は作成する
if not os.path.exists(save_dir):
    try:
        os.makedirs(save_dir)
        print(f"ディレクトリを作成しました: {save_dir}")
    except OSError as e:
        print(f"⚠️ ディレクトリ作成エラー: {e}")

# フルパスの生成
output_path = os.path.join(save_dir, output_filename)

# --- プロット準備 ---
fig = plt.figure(figsize=(10, 6))

# ★修正1: 描画領域をギリギリまで広げる [left, bottom, width, height]
ax = fig.add_axes([0.13, 0.13, 0.86, 0.86]) 

for config in files_config:
    try:
        filename = config['filename']
        dt = config['dt']
        
        # データの読み込み
        df = pd.read_csv(filename, header=None, sep='\s+')
        
        # データを取り出す (このファイル形式では1列目がエネルギーと仮定)
        energy = df.iloc[:, 0] 
        
        # 時間軸(X軸)を生成
        time_axis = np.arange(len(energy)) * dt
        
        # プロット
        ax.plot(time_axis, energy, 
                label=config['label'], 
                linewidth=2.5,  
                alpha=0.8)
        
        print(f"'{filename}' をプロットしました。")

    except FileNotFoundError:
        print(f"⚠️ エラー: '{filename}' が見つかりません。")
    except Exception as e:
        print(f"⚠️ エラー ({filename}): {e}")

# --- グラフの体裁 ---

# ★修正2: 文字サイズを超特大に
ax.set_xlabel('Time [s]', fontsize=16)
ax.set_ylabel(r'$E_{\mathrm{total}}$ [-]', fontsize=16)

# 目盛りの数字
ax.tick_params(axis='both', labelsize=16)

# グリッド
ax.grid(True, which='both', linestyle='--', alpha=0.7)

# ★修正3: 凡例の枠を消す & 文字大きく
ax.legend(fontsize=16, loc='upper right', frameon=False)

# --- 保存 ---
# PDF形式で指定のパスに保存
plt.savefig(output_path)
print(f"\nグラフを以下に保存しました:\n{output_path}")