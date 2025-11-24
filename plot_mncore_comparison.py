import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- 設定 ---
file_double = 'baneljdoubleresult.txt'  # MN-Core 倍精度
file_float  = 'baneljfloatresult.txt'   # MN-Core 単精度

output_image = 'mncore_double_vs_float.png'

# 列名
columns = ['Time', 'Pos', 'PotentialE', 'KineticE', 'TotalE']

# --- データ読み込み関数 ---
def load_data(filename):
    try:
        # タブ区切り(\t)で読み込み、コメント行(#)は無視
        df = pd.read_csv(filename, sep='\t', header=None, names=columns, comment='#')
        return df['Time'], df['TotalE']
    except FileNotFoundError:
        print(f"エラー: '{filename}' が見つかりません。")
        return None, None
    except Exception as e:
        print(f"エラー ({filename}): {e}")
        return None, None

# --- メイン処理 ---

# データを取得
t_d, e_d = load_data(file_double)
t_f, e_f = load_data(file_float)

if t_d is not None and e_d is not None:
    # キャンバス準備 (余白ギリギリ・特大文字)
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.18, 0.15, 0.78, 0.82]) 

    # --- プロット ---
    
    # MN-Core Double (オレンジ・実線)
    ax.plot(t_d, e_d, label='MN-Core (Double)', linewidth=3.0, linestyle='-', color='tab:orange', alpha=0.9)
    
    # MN-Core Float (緑・実線) - データがあればプロット
    if t_f is not None and e_f is not None:
        # データ点数を合わせる
        min_len = min(len(t_d), len(t_f))
        ax.plot(t_f[:min_len], e_f[:min_len], label='MN-Core (Float)', linewidth=3.0, linestyle='-', color='tab:green', alpha=0.7)

    # --- グラフの体裁 ---
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('Total Energy', fontsize=28)
    
    ax.tick_params(axis='both', labelsize=22)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # オフセット表記を無効化 (数値そのままで表示)
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    # 凡例 (枠なし・特大)
    ax.legend(fontsize=20, loc='best', frameon=False)
    
    # 保存
    plt.savefig(output_image)
    print(f"グラフを '{output_image}' として保存しました。")

else:
    print("プロットするデータがありませんでした。")
