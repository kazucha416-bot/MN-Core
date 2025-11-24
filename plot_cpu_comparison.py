import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker # 目盛り調整用

# --- 設定 ---
file_double = 'lj_oscillator_1D.txt'        # 倍精度
file_float  = 'lj_oscillator_1D_float.txt'  # 単精度
output_image = 'cpu_double_vs_float_fixed.png'

# --- データ読み込み関数 ---
def load_data(filename):
    try:
        df = pd.read_csv(filename, sep='\s+', header=None, comment='#')
        # 0列目: Time, 4列目: TotalE
        return df.iloc[:, 0], df.iloc[:, 4]
    except Exception as e:
        print(f"エラー ({filename}): {e}")
        return None, None

# --- メイン処理 ---
t_d, e_d = load_data(file_double)
t_f, e_f = load_data(file_float)

if t_d is not None and t_f is not None:
    fig = plt.figure(figsize=(10, 6))
    # 左余白を広めに確保 (桁数が増えるため)
    ax = fig.add_axes([0.20, 0.15, 0.75, 0.82]) 

    # プロット
    ax.plot(t_d, e_d, label='CPU (Double)', linewidth=3.0, linestyle='-', color='tab:blue', alpha=0.8)
    
    # データ点数を合わせてプロット
    min_len = min(len(t_d), len(t_f))
    ax.plot(t_f[:min_len], e_f[:min_len], label='CPU (Float)', linewidth=3.0, linestyle='--', color='tab:purple', alpha=0.8)
    
    # --- グラフの体裁 ---
    ax.set_xlabel('Time', fontsize=28)
    ax.set_ylabel('Total Energy', fontsize=28)
    
    ax.tick_params(axis='both', labelsize=18) # 文字サイズ
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # ★重要: オフセット表記を無効化して、そのままの数値を表示する
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    # 凡例
    ax.legend(fontsize=20, loc='best', frameon=False)
    
    plt.savefig(output_image)
    print(f"グラフを '{output_image}' として保存しました。\n(Y軸のオフセット表記を無効化しました)")

else:
    print("データが読み込めませんでした。")
