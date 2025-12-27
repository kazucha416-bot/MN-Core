import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

# --- 設定 ---
file_double = 'lj_oscillator_1D.txt'        # 倍精度
file_float  = 'lj_oscillator_1D_float.txt'  # 単精度

# 保存先のディレクトリとファイル名
output_dir = '/home/kazuki/thesis/images' 
output_filename = 'cpu_double_vs_float_fixed.pdf'
output_path = os.path.join(output_dir, output_filename)

# --- データ読み込み関数 ---
def load_data(filename):
    try:
        # 正規表現の警告が出ないように r'\s+' にしています
        df = pd.read_csv(filename, sep=r'\s+', header=None, comment='#')
        return df.iloc[:, 0], df.iloc[:, 4]
    except Exception as e:
        print(f"エラー ({filename}): {e}")
        return None, None

# --- メイン処理 ---
t_d, e_d = load_data(file_double)
t_f, e_f = load_data(file_float)

if t_d is not None and t_f is not None:
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_axes([0.20, 0.15, 0.75, 0.82]) 

    # プロット 1: 倍精度 (Double) -> 赤色・実線
    ax.plot(t_d, e_d, label='CPU (Double)', linewidth=3.0, linestyle='-', color='tab:red', alpha=0.8)
    
    # プロット 2: 単精度 (Float) -> 青色・実線
    # データ点数を合わせてプロット
    min_len = min(len(t_d), len(t_f))
    ax.plot(t_f[:min_len], e_f[:min_len], label='CPU (Float)', linewidth=3.0, linestyle='-', color='tab:blue', alpha=0.8)
    
    # --- グラフの体裁 ---
    # ★単位 [s] を追加
    ax.set_xlabel('Time [s]', fontsize=28)
    ax.set_ylabel('Total Energy', fontsize=28)
    
    ax.tick_params(axis='both', labelsize=18)
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # オフセット表記を無効化
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)

    # 凡例
    ax.legend(fontsize=20, loc='best', frameon=False)
    
    # --- 保存処理 ---
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_path)
    print(f"グラフを '{output_path}' として保存しました。")

else:
    print("データが読み込めませんでした。")