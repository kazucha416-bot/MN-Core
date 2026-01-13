import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_comparison_separate():
    # ==========================================
    # ★設定パラメータ
    # ==========================================
    legend_fontsize = 20  # 凡例のフォントサイズ (ここをいじると大きさが変わります)
    
    # --- 保存先ディレクトリの設定 ---
    save_dir = r'/home/kazuki/thesis/images'
    
    # ディレクトリが存在しない場合は作成する
    os.makedirs(save_dir, exist_ok=True)

    # --- 読み込むファイル名の設定 ---
    # ※ 必要に応じてファイル名を変更してください
    cpu_file = '0113mdfree4_cpu_result_float_3000.txt' # cpuの方は2001ステップにする
    mn_core_file = '0113mdfree4_mncore_3000results.txt'

    # --- データの読み込み ---
    try:
        # CPUデータ: ヘッダーなし
        cpu_df = pd.read_csv(cpu_file, sep='\s+', header=None, 
                             names=['Time', 'Potential', 'Kinetic', 'Total'])
        # MN-Coreデータ: ヘッダーあり、スキップ2行
        mn_df = pd.read_csv(mn_core_file, sep='\s+', skiprows=2, 
                            names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = mn_df.apply(pd.to_numeric, errors='coerce').dropna()
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # --- 共通のプロット関数 ---
    def save_single_plot(x_cpu, y_cpu, label_cpu, color_cpu, 
                         x_mn, y_mn, label_mn, color_mn, marker_mn, 
                         ylabel, filename, legend_size):
        
        # 図のサイズ設定
        plt.figure(figsize=(10, 6))
        
        # プロット
        # CPU: 実線
        plt.plot(x_cpu, y_cpu, label=label_cpu, color=color_cpu, 
                 alpha=0.6, linewidth=1.5)
        
        # MN-Core: 点線 + マーカー
        plt.plot(x_mn, y_mn, label=label_mn, color=color_mn, 
                 linestyle='--', marker=marker_mn, markersize=4, linewidth=1.5)
        
        # タイトルはなし (plt.title削除)
        
        # ラベル設定
        plt.xlabel('Time [s]')
        plt.ylabel(ylabel)
        
        # 凡例 (★ここでサイズを指定)
        plt.legend(loc='best', fontsize=legend_size)
        
        plt.grid(True)
        plt.tight_layout()
        
        # 保存
        save_path = os.path.join(save_dir, filename)
        plt.savefig(save_path)
        plt.close()
        print(f"グラフを保存しました: {save_path}")

    # 1. 全エネルギー
    save_single_plot(cpu_df['Time'], cpu_df['Total'], 'CPU', 'black',
                     mn_df['Time'], mn_df['Total'], 'MN-Core', 'red', 'o',
                     'Total Energy', 'TotalEnergy_split.pdf', legend_fontsize)

    # 2. ポテンシャルエネルギー
    save_single_plot(cpu_df['Time'], cpu_df['Potential'], 'CPU', 'blue',
                     mn_df['Time'], mn_df['Potential'], 'MN-Core', 'orange', 'x',
                     'Energy', 'PotentialEnergy_split.pdf', legend_fontsize)

    # 3. 運動エネルギー
    save_single_plot(cpu_df['Time'], cpu_df['Kinetic'], 'CPU', 'green',
                     mn_df['Time'], mn_df['Kinetic'], 'MN-Core', 'purple', '^',
                     'Energy', 'KineticEnergy_split.pdf', legend_fontsize)

if __name__ == "__main__":
    plot_comparison_separate()