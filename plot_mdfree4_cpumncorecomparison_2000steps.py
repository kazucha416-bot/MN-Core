import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_comparison_separate():
    # --- 保存先ディレクトリの設定 ---
    save_dir = r'/home/kazuki/thesis/images'
    
    # ディレクトリが存在しない場合は作成する
    os.makedirs(save_dir, exist_ok=True)

    # --- 読み込むファイル名の設定 ---
    # ※ 必要に応じてファイル名を変更してください
    cpu_file = 'mdfree4_cpu_result_float.txt' 
    mn_core_file = '0109_freemd4_mncore_finalresults.txt'

    # --- データの読み込み ---
    try:
        cpu_df = pd.read_csv(cpu_file, sep='\s+', header=None, 
                             names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = pd.read_csv(mn_core_file, sep='\s+', skiprows=2, 
                            names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = mn_df.apply(pd.to_numeric, errors='coerce').dropna()
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # --- 共通のプロット関数 ---
    def save_single_plot(x_cpu, y_cpu, label_cpu, color_cpu, 
                         x_mn, y_mn, label_mn, color_mn, marker_mn, 
                         title, ylabel, filename):
        plt.figure(figsize=(10, 6))
        
        # CPU Plot
        plt.plot(x_cpu, y_cpu, label=label_cpu, color=color_cpu, 
                 alpha=0.6, linewidth=1)
        
        # MN-Core Plot
        plt.plot(x_mn, y_mn, label=label_mn, color=color_mn, 
                 linestyle='--', marker=marker_mn, markersize=4)
        
        plt.title(title)
        plt.xlabel('Time [s]')
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # 保存パスの結合
        save_path = os.path.join(save_dir, filename)
        plt.savefig(save_path)
        plt.close() # メモリ解放
        print(f"グラフを保存しました: {save_path}")

    # 1. 全エネルギー (Total Energy)
    save_single_plot(cpu_df['Time'], cpu_df['Total'], 'CPU (Reference)', 'black',
                     mn_df['Time'], mn_df['Total'], 'MN-Core', 'red', 'o',
                     'Total Energy Conservation', 'Total Energy', 'TotalEnergy_split.pdf')

    # 2. ポテンシャルエネルギー (Potential Energy)
    save_single_plot(cpu_df['Time'], cpu_df['Potential'], 'CPU', 'blue',
                     mn_df['Time'], mn_df['Potential'], 'MN-Core', 'orange', 'x',
                     'Potential Energy', 'Energy', 'PotentialEnergy_split.pdf')

    # 3. 運動エネルギー (Kinetic Energy)
    save_single_plot(cpu_df['Time'], cpu_df['Kinetic'], 'CPU', 'green',
                     mn_df['Time'], mn_df['Kinetic'], 'MN-Core', 'purple', '^',
                     'Kinetic Energy', 'Energy', 'KineticEnergy_split.pdf')

if __name__ == "__main__":
    plot_comparison_separate()