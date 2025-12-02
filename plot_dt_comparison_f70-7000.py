import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 設定 ---
files_config = [
    # { 'filename': 'ファイル名', 'dt': 時間刻み幅, 'label': '凡例ラベル' }
    {'filename': 'resultnew_f70.txt',   'dt': 0.1,   'label': 'dt=0.1 s'},
    {'filename': 'result_f700.txt',  'dt': 0.01,  'label': 'dt=0.01 s'},
    {'filename': 'result_f7000.txt', 'dt': 0.001, 'label': 'dt=0.001 s'},
]

output_image = 'energy_comparison_dt_final.png'

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
        
        # データを取り出す (1列目)
        energy = df.iloc[:, 0] 
        
        # 時間軸(X軸)を生成
        time_axis = np.arange(len(energy)) * dt
        
        # プロット
        ax.plot(time_axis, energy, 
                label=config['label'], 
                linewidth=3.0,  # 線も太く (3.0)
                alpha=0.8)
        
        print(f"'{filename}' をプロットしました。")

    except FileNotFoundError:
        print(f"⚠️ エラー: '{filename}' が見つかりません。")
    except Exception as e:
        print(f"⚠️ エラー ({filename}): {e}")

# --- グラフの体裁 ---

# ★修正2: 文字サイズを超特大に
ax.set_xlabel('Time (s)', fontsize=28)
ax.set_ylabel('$\mathrm{E}_{\mathrm{total}}$', fontsize=28)

# 目盛りの数字
ax.tick_params(axis='both', labelsize=22)

# グリッド
ax.grid(True, which='both', linestyle='--', alpha=0.7)

# ★修正3: 凡例の枠を消す & 文字大きく
ax.legend(fontsize=16,loc='upper right', frameon=False)

# --- 保存 ---
plt.savefig(output_image)
print(f"\nグラフを '{output_image}' として保存しました。")
