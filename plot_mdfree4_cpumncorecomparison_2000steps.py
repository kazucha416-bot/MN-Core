import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_comparison_separate():
    # ==========================================
    # ★設定パラメータ
    # ==========================================
    legend_fontsize = 20  # 凡例のフォントサイズ
    label_fontsize = 16   # 軸ラベル（Time [s]など）のフォントサイズ
    tick_fontsize = 16    # 軸の数字（目盛り）のフォントサイズ
    
    # --- 保存先ディレクトリの設定 ---
    save_dir = r'/home/kazuki/thesis/images'
    
    # ディレクトリが存在しない場合は作成する
    os.makedirs(save_dir, exist_ok=True)

    # --- 読み込むファイル名の設定 ---
    cpu_file = '0113mdfree4_cpu_result_float_3000.txt' 
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
                         x_mn, y_mn, label_mn, color_mn, 
                         ylabel, filename, legend_size):
        
        # 図のサイズ設定
        plt.figure(figsize=(10, 6))
        
        # プロット
        # CPU: 実線
        plt.plot(x_cpu, y_cpu, label=label_cpu, color=color_cpu, 
                 linestyle='-', linewidth=2.0, alpha=0.7)
        
        # MN-Core: 破線 (マーカーなし)
        # ★ここを修正しました: marker引数を削除
        plt.plot(x_mn, y_mn, label=label_mn, color=color_mn, 
                 linestyle='--', linewidth=2.5, alpha=0.9)
        
        # ラベル設定
        plt.xlabel('Time [s]', fontsize=label_fontsize)
        plt.ylabel(ylabel, fontsize=label_fontsize)
        
        # 軸の数字（目盛り）の設定
        plt.tick_params(labelsize=tick_fontsize)
        
        # 凡例
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
                     mn_df['Time'], mn_df['Total'], 'MN-Core', 'red',
                     r'$E_{\mathrm{total}}$', 'TotalEnergy_split.pdf', legend_fontsize)

    # 2. ポテンシャルエネルギー
    save_single_plot(cpu_df['Time'], cpu_df['Potential'], 'CPU', 'blue',
                     mn_df['Time'], mn_df['Potential'], 'MN-Core', 'orange',
                     r'$E_{\mathrm{potential}}$', 'PotentialEnergy_split.pdf', legend_fontsize)

    # 3. 運動エネルギー
    save_single_plot(cpu_df['Time'], cpu_df['Kinetic'], 'CPU', 'green',
                     mn_df['Time'], mn_df['Kinetic'], 'MN-Core', 'purple',
                     r'$E_{\mathrm{kinetic}}$', 'KineticEnergy_split.pdf', legend_fontsize)

if __name__ == "__main__":
    plot_comparison_separate()