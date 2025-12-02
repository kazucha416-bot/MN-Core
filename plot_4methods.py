import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 設定 ---
files_config = [
    {"file": "result_Euler70.txt", "label": "Euler",           "color": "tab:blue",   "style": "--"},
    {"file": "resultVV70.txt",     "label": "VV", "color": "tab:green",  "style": "-"},
    {"file": "result_RK270.txt",   "label": "RK2",             "color": "tab:orange", "style": "-."},
    {"file": "result_RK470.txt",   "label": "RK4",             "color": "tab:red",    "style": ":"},
]

output_image = 'comparison_4methods_final.png'
dt_default = 0.1 

# --- プロット準備 ---
fig = plt.figure(figsize=(10, 6))

# ★修正1: 描画領域をギリギリまで広げる [left, bottom, width, height]
# 文字が大きいため、はみ出さない最小限の余白(0.13)だけ確保し、残りをすべてグラフにします
ax = fig.add_axes([0.13, 0.13, 0.86, 0.86]) 

for config in files_config:
    filename = config['file']
    label_name = config['label']
    
    try:
        df = pd.read_csv(filename, sep='\s+', header=None, comment='#')
        
        if df.shape[1] >= 5:
            time_data = df.iloc[:, 0]
            energy_data = df.iloc[:, 4]
        else:
            energy_data = df.iloc[:, 0]
            time_data = np.arange(len(energy_data)) * dt_default

        ax.plot(time_data, energy_data, 
                 label=label_name, 
                 color=config['color'], 
                 linestyle=config['style'], 
                 linewidth=3.0,  # 線もさらに太く(2.5 -> 3.0)
                 alpha=0.8)
                 
        print(f"'{filename}' をプロットしました。")

    except FileNotFoundError:
        print(f"⚠️ エラー: '{filename}' が見つかりません。")
    except Exception as e:
        print(f"⚠️ エラー ({filename}): {e}")

# --- グラフの体裁 ---

# ★修正2: 文字サイズをさらに大きく
ax.set_xlabel('Time (s)', fontsize=28)
ax.set_ylabel('$\mathrm{E}_{\mathrm{total}}$', fontsize=28)

# 目盛りの数字
ax.tick_params(axis='both', labelsize=22)

# グリッド
ax.grid(True, which='both', linestyle='--', alpha=0.7)

# ★修正3: 凡例の枠を消す (frameon=False)
# 文字サイズも大きく (14 -> 18)
ax.legend(fontsize=18, loc='best', frameon=False)

# --- 保存 ---
plt.savefig(output_image)
print(f"\nグラフを '{output_image}' として保存しました。")
