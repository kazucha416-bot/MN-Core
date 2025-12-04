import pandas as pd
import matplotlib.pyplot as plt

# --- 設定 ---
file_A = 'lj_oscillator_1D.txt'               # (1) CPU Double
file_B = 'lj_oscillator_1D_float.txt'         # (2) CPU Float (新規追加)
file_C = 'baneljdoubleresult2000steps.txt'    # (3) MN-Core2 Double
file_D = 'baneljfloat2000stepsresult.txt'     # (4) MN-Core2 Float

output_image = 'lj_comparison_4methods.png'

# ファイルA, Bの列名 (Time, Pos, PE, KE, TotalE) -> 5列形式
columns_AB = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']
# ファイルC, Dの列名 (TotalEのみ)
columns_CD = ['TotalE_MNCORE']

# --- データ読み込み ---
try:
    # A: CPU (Double)
    data_A = pd.read_csv(
        file_A, 
        sep='\s+', 
        header=None, 
        names=columns_AB, 
        comment='#'
    )
    print(f"'{file_A}' を読み込みました。 (全 {len(data_A)} 行)")

    # B: CPU (Float) [追加]
    data_B = pd.read_csv(
        file_B, 
        sep='\s+', 
        header=None, 
        names=columns_AB, 
        comment='#'
    )
    print(f"'{file_B}' を読み込みました。 (全 {len(data_B)} 行)")

    # C: MN-Core2 (Double)
    data_C = pd.read_csv(
        file_C, 
        header=None, 
        names=columns_CD
    )
    print(f"'{file_C}' を読み込みました。 (全 {len(data_C)} 行)")

    # D: MN-Core2 (Float)
    data_D = pd.read_csv(
        file_D, 
        header=None, 
        names=columns_CD
    )
    print(f"'{file_D}' を読み込みました。 (全 {len(data_D)} 行)")

    # --- グラフ作成準備 ---
    
    # データ点数を最も短いものに合わせる
    num_points = min(len(data_A), len(data_B), len(data_C), len(data_D))
    
    # データをスライス (時間軸はAを使用)
    time_axis = data_A['Time'].head(num_points)
    
    totalE_A = data_A['TotalE'].head(num_points)
    totalE_B = data_B['TotalE'].head(num_points) # CPU Float
    totalE_C = data_C['TotalE_MNCORE'].head(num_points)
    totalE_D = data_D['TotalE_MNCORE'].head(num_points)

    # ★スタイル統一: キャンバス準備
    fig = plt.figure(figsize=(10, 6))
    
    # ★スタイル統一: 描画領域をギリギリまで広げる
    # Y軸ラベルのために左余白を少し多め(0.18)にとっています
    ax = fig.add_axes([0.18, 0.13, 0.81, 0.86]) 

    # --- プロット ---
    
    # 1. CPU (Double) -> 青, 破線
    ax.plot(time_axis, totalE_A, label='CPU (Double)', linestyle='--', linewidth=3.0, color='tab:blue')

    # 2. CPU (Float) -> 紫, 点線 (新規)
    ax.plot(time_axis, totalE_B, label='CPU (Float)', linestyle=':', linewidth=3.0, color='tab:purple')
    
    # 3. MN-Core2 (Double) -> オレンジ, 実線
    ax.plot(time_axis, totalE_C, label='MN-Core 2 (Double)', linewidth=3.0, color='tab:orange')

    # 4. MN-Core2 (Float) -> 緑, 実線
    ax.plot(time_axis, totalE_D, label='MN-Core 2 (Float)', linewidth=3.0, color='tab:green', alpha=0.8)
    
    # --- グラフの体裁 (超特大文字) ---
    
    # 軸ラベル
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('$\mathrm{E}_{\mathrm{total, LJ}}$', fontsize=28)
    
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
