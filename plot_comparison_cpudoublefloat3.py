import pandas as pd
import matplotlib.pyplot as plt

# --- 設定 ---
file_A = 'lj_oscillator_1D.txt'             # (CPU)
file_B = 'baneljdoubleresult2000steps.txt'  # (MN-Core2 Double)
file_C = 'baneljfloat2000stepsresult.txt'   # (MN-Core2 Float)

output_image = 'lj_comparison_3methods.png'

# ファイルAの列名 (Time, Pos, PE, KE, TotalE)
columns_A = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']
# ファイルB, Cの列名 (TotalEのみ)
columns_BC = ['TotalE_MNCORE']

# --- データ読み込み ---
try:
    # A: CPU
    data_A = pd.read_csv(
        file_A, 
        sep='\s+', 
        header=None, 
        names=columns_A, 
        comment='#'
    )
    print(f"'{file_A}' を読み込みました。 (全 {len(data_A)} 行)")

    # B: MN-Core2 Double
    data_B = pd.read_csv(
        file_B, 
        header=None, 
        names=columns_BC
    )
    print(f"'{file_B}' を読み込みました。 (全 {len(data_B)} 行)")

    # C: MN-Core2 Float
    data_C = pd.read_csv(
        file_C, 
        header=None, 
        names=columns_BC
    )
    print(f"'{file_C}' を読み込みました。 (全 {len(data_C)} 行)")

    # --- グラフ作成準備 ---
    
    # データ点数を最も短いものに合わせる (基本は2000で揃っているはず)
    num_points = min(len(data_A), len(data_B), len(data_C))
    
    # データをスライス
    time_axis = data_A['Time'].head(num_points)
    totalE_A = data_A['TotalE'].head(num_points)
    totalE_B = data_B['TotalE_MNCORE'].head(num_points)
    totalE_C = data_C['TotalE_MNCORE'].head(num_points)

    # ★スタイル統一: キャンバス準備
    fig = plt.figure(figsize=(10, 6))
    
    # ★スタイル統一: 描画領域をギリギリまで広げる
    # Y軸ラベルのために左余白を少し多め(0.18)にとっています
    ax = fig.add_axes([0.18, 0.13, 0.81, 0.86]) 

    # --- プロット ---
    
    # 1. CPU (点線、青)
    ax.plot(time_axis, totalE_A, label='CPU (Double)', linestyle='--', linewidth=3.0, color='tab:blue')
    
    # 2. MN-Core2 Double (実線、オレンジ)
    ax.plot(time_axis, totalE_B, label='MN-Core2 (Double)', linewidth=3.0, color='tab:orange')

    # 3. MN-Core2 Float (実線、緑) -> ★追加
    ax.plot(time_axis, totalE_C, label='MN-Core2 (Float)', linewidth=3.0, color='tab:green', alpha=0.8)
    
    # --- グラフの体裁 (超特大文字) ---
    
    # 軸ラベル
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('Total Energy', fontsize=28)
    
    # 目盛りの数字
    ax.tick_params(axis='x', labelsize=22)
    ax.tick_params(axis='y', labelsize=18) # Y軸は桁数が多いので少し小さめ
    
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
