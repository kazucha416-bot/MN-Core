import pandas as pd
import matplotlib.pyplot as plt

# --- 設定 ---
file_double = 'baneljdoubleresult.txt'  # 倍精度データ
file_float  = 'baneljfloatresult.txt'   # 単精度データ

output_image = 'mncore_double_vs_float_energies.png'

# 列名
columns = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']

# --- データ読み込み ---
try:
    # Doubleデータの読み込み
    df_d = pd.read_csv(
        file_double, 
        sep='\t', 
        header=0, 
        names=columns, 
        comment='#'
    )
    print(f"'{file_double}' を読み込んでいます... (全 {len(df_d)} 行)")

    # Floatデータの読み込み
    df_f = pd.read_csv(
        file_float, 
        sep='\t', 
        header=0, 
        names=columns, 
        comment='#'
    )
    print(f"'{file_float}' を読み込んでいます... (全 {len(df_f)} 行)")

    # --- グラフ作成準備 ---
    # データ点数を短い方に合わせる
    num_points = min(len(df_d), len(df_f))
    
    # データをスライス
    time_axis = df_d['Time'].head(num_points)
    
    pe_d = df_d['PotentialE'].head(num_points)
    ke_d = df_d['KineticE'].head(num_points)
    total_d = df_d['TotalE'].head(num_points)
    
    pe_f = df_f['PotentialE'].head(num_points)
    ke_f = df_f['KineticE'].head(num_points)
    total_f = df_f['TotalE'].head(num_points)

    # ★スタイル統一: キャンバス準備
    fig = plt.figure(figsize=(10, 6))
    
    # ★スタイル統一: 描画領域をギリギリまで広げる
    ax = fig.add_axes([0.13, 0.13, 0.86, 0.86]) 

    # --- プロット (6本) ---
    
    # 1. Potential Energy (青)
    ax.plot(time_axis, pe_d, label='PE (Double)', linewidth=3.0, linestyle='-', color='tab:blue', alpha=0.8)
    ax.plot(time_axis, pe_f, label='PE (Float)',  linewidth=2.5, linestyle='--', color='tab:blue', alpha=0.6)
    
    # 2. Kinetic Energy (緑)
    ax.plot(time_axis, ke_d, label='KE (Double)', linewidth=3.0, linestyle='-', color='tab:green', alpha=0.8)
    ax.plot(time_axis, ke_f, label='KE (Float)',  linewidth=2.5, linestyle='--', color='tab:green', alpha=0.6)
    
    # 3. Total Energy (赤)
    ax.plot(time_axis, total_d, label='Total (Double)', linewidth=3.0, linestyle='-', color='tab:red', alpha=0.9)
    ax.plot(time_axis, total_f, label='Total (Float)',  linewidth=2.5, linestyle='--', color='tab:red', alpha=0.7)
    
    # --- グラフの体裁 (超特大文字) ---
    
    # 軸ラベル
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('Energy', fontsize=28)
    
    # 目盛りの数字
    ax.tick_params(axis='both', labelsize=22)
    
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # 凡例 (枠なし・特大)
    # 線が多いので、邪魔にならない位置に配置するか、外に出すのもアリですが、
    # とりあえず 'best' で配置します
    ax.legend(fontsize=16, loc='best', frameon=False, ncol=2) # 2列にしてコンパクトに
    
    # --- ファイルに保存 ---
    plt.savefig(output_image)
    print(f"比較グラフを '{output_image}' として保存しました。")

except FileNotFoundError as e:
    print(f"エラー: {e.filename} が見つかりません。")
except Exception as e:
    print(f"エラーが発生しました: {e}")
