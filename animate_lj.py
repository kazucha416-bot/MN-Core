import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# --- 設定 ---
filename = 'lj_oscillator_1D.txt' # 読み込むファイル
output_file = 'lj_animation.mp4'  # 保存する動画ファイル名 (または .gif)
skip_step = 10                    # 描画を間引くステップ数 (大きくすると動画が短く/速くなる)

# --- データ読み込み ---
try:
    # 5列のデータを読み込む
    columns = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']
    df = pd.read_csv(filename, sep='\s+', header=None, names=columns, comment='#')
    
    # データを間引く (全部描画すると遅いため)
    data = df.iloc[::skip_step, :].reset_index(drop=True)
    
    times = data['Time'].values
    positions = data['Pos'].values
    total_e = data['TotalE'].values

except FileNotFoundError:
    print(f"エラー: '{filename}' が見つかりません。")
    exit()

# --- アニメーションの準備 ---
fig = plt.figure(figsize=(10, 8))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1])

# 上のグラフ: 粒子の動き (1次元)
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_xlim(0.8, 2.5) # X軸の範囲 (粒子の動く範囲に合わせて調整してください)
ax1.set_ylim(-1, 1)    # Y軸は見た目用
ax1.set_xlabel('Position (r)')
ax1.set_title('Particle Motion (1D LJ Potential)')
ax1.get_yaxis().set_visible(False) # Y軸の目盛りを消す
ax1.grid(True, axis='x')

# 固定粒子 (原点)
ax1.plot(0, 0, 'ko', markersize=15, label='Fixed Particle')
# 動く粒子 (初期位置)
particle, = ax1.plot([], [], 'o', markersize=20, color='tab:orange', label='Moving Particle')
# 軌跡線
trail, = ax1.plot([], [], '-', color='tab:orange', alpha=0.5)

ax1.legend()

# 下のグラフ: エネルギーの時間変化
ax2 = fig.add_subplot(gs[1, 0])
ax2.set_xlim(times[0], times[-1])
# エネルギーの振れ幅に合わせてY軸を調整 (少し余裕を持たせる)
e_mean = np.mean(total_e)
e_range = max(np.ptp(total_e), 0.01) # ptp = max - min
ax2.set_ylim(e_mean - e_range*2, e_mean + e_range*2)

ax2.set_xlabel('Time')
ax2.set_ylabel('Total Energy')
ax2.set_title('Total Energy Evolution')
ax2.grid(True)

# エネルギー線
energy_line, = ax2.plot([], [], '-', color='tab:blue', linewidth=2)

# --- 更新関数 ---
def update(frame):
    # 現在のフレームのデータ
    current_time = times[frame]
    current_pos = positions[frame]
    
    # 1. 粒子の位置を更新
    particle.set_data([current_pos], [0])
    
    # 軌跡 (少し過去まで表示)
    trail_length = 50
    start = max(0, frame - trail_length)
    trail.set_data(positions[start:frame+1], np.zeros(frame+1-start))

    # 2. エネルギーグラフを更新
    energy_line.set_data(times[:frame+1], total_e[:frame+1])
    
    return particle, trail, energy_line

# --- アニメーション作成 ---
# frames=len(data) : フレーム総数
# interval=30 : 1フレームの表示時間(ms)
ani = animation.FuncAnimation(fig, update, frames=len(data), interval=30, blit=True)

# --- 保存 ---
print("アニメーションを作成中... (少し時間がかかります)")

# mp4で保存する場合 (要 ffmpeg)
try:
    ani.save(output_file, writer='ffmpeg', fps=30)
    print(f"'{output_file}' に保存しました。")
except Exception as e:
    print("mp4保存に失敗しました (ffmpegがない可能性があります)。GIFで保存します。")
    ani.save('lj_animation.gif', writer='pillow', fps=30)
    print("'lj_animation.gif' に保存しました。")

# plt.show() # ウィンドウで見たい場合はコメントアウトを外す
