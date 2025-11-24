import pandas as pd
import matplotlib.pyplot as plt

# --- 設定 ---
filename = 'lj_oscillator_1D.txt'
output_image = 'lj_all_energies.png'

# 列名 (Time, Pos, PE, KE, TotalE)
columns = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']

# --- データ読み込み ---
try:
    df = pd.read_csv(
        filename, 
        sep='\s+', 
        header=None, 
        names=columns, 
        comment='#'
    )
    print(f"'{filename}' を読み込みました。 (全 {len(df)} 行)")

    # --- グラフ作成準備 ---
    time_axis = df['Time']
    pe = df['PotentialE']
    ke = df['KineticE']
    total_e = df['TotalE']

    # ★スタイル統一: キャンバス準備
    fig = plt.figure(figsize=(10, 6))
    
    # ★スタイル統一: 描画領域をギリギリまで広げる
    ax = fig.add_axes([0.18, 0.13, 0.81, 0.86]) 

    # --- プロット (3本) ---
    
    # 1. Potential Energy (青・破線)
    ax.plot(time_axis, pe, label='Potential Energy', linewidth=3.0, linestyle='--', color='tab:blue')
    
    # 2. Kinetic Energy (緑・点線)
    ax.plot(time_axis, ke, label='Kinetic Energy', linewidth=3.0, linestyle=':', color='tab:green')
    
    # 3. Total Energy (赤・実線)
    ax.plot(time_axis, total_e, label='Total Energy', linewidth=3.0, linestyle='-', color='tab:red')
    
    # --- グラフの体裁 (超特大文字) ---
    
    # 軸ラベル
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('Energy', fontsize=28)
    
    # 目盛りの数字
    ax.tick_params(axis='both', labelsize=22)
    
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # 凡例 (枠なし・特大)
    # 3本あるので見やすい位置(best)に配置
    ax.legend(fontsize=18, loc='best', frameon=False)
    
    # --- ファイルに保存 ---
    plt.savefig(output_image)
    print(f"グラフを '{output_image}' として保存しました。")

except FileNotFoundError:
    print(f"エラー: '{filename}' が見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
