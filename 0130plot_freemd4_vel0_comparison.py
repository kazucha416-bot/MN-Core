import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_comparison_separate():
    # ==========================================
    # ★設定パラメータ
    # ==========================================
    legend_fontsize = 20  # 凡例のフォントサイズ
    label_fontsize = 16   # 軸ラベルのフォントサイズ
    tick_fontsize = 16    # 軸の数字のフォントサイズ
    
    # --- 保存先ディレクトリの設定 ---
    save_dir = r'/home/kazuki/thesis/images/'
    
    # ディレクトリが存在しない場合は作成する
    os.makedirs(save_dir, exist_ok=True)

    # --- 読み込むファイル名の設定 ---
    cpu_file = '0130mdfree4_cpuresult_vel0.txt' 
    mn_core_file = '0205_freemd4_v=3.0_decimal.txt'

    # --- データの読み込み ---
    try:
        # sep=r'\s+' に修正 (警告回避)
        cpu_df = pd.read_csv(cpu_file, sep=r'\s+', header=None, 
                             names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = pd.read_csv(mn_core_file, sep=r'\s+', skiprows=2, 
                            names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = mn_df.apply(pd.to_numeric, errors='coerce').dropna()
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # --- 共通のプロット関数 ---
    def save_single_plot(x_cpu, y_cpu, label_cpu, color_cpu, 
                         x_mn, y_mn, label_mn, color_mn, 
                         ylabel, filename, legend_size, plot_as_points=False):
        
        # 図のサイズ設定
        plt.figure(figsize=(10, 6))
        
        if plot_as_points:
            # プロット（点）モード
            plt.plot(x_cpu, y_cpu, label=label_cpu, color=color_cpu, 
                     linestyle='None', marker='o', markersize=3, alpha=0.6)
            plt.plot(x_mn, y_mn, label=label_mn, color=color_mn, 
                     linestyle='None', marker='x', markersize=3, alpha=0.8)
        else:
            # ★線モード (全てこれを使います)
            # CPU: 実線
            plt.plot(x_cpu, y_cpu, label=label_cpu, color=color_cpu, 
                     linestyle='-', linewidth=2.0, alpha=0.7)
            
            # MN-Core: 破線
            plt.plot(x_mn, y_mn, label=label_mn, color=color_mn, 
                     linestyle='--', linewidth=2.5, alpha=0.9)
        
        # ラベル設定
        plt.xlabel('Time [-]', fontsize=label_fontsize)
        plt.ylabel(ylabel, fontsize=label_fontsize)
        
        # 軸の数字（目盛り）の設定
        plt.tick_params(labelsize=tick_fontsize)
        
        # 凡例 (グラフの上に横並び配置)
        plt.legend(bbox_to_anchor=(0.5, 1.05), loc='lower center', borderaxespad=0, 
                   ncol=3, fontsize=16, frameon=False)
        
        plt.grid(True)
        plt.tight_layout()
        
        # 保存
        save_path = os.path.join(save_dir, filename)
        plt.savefig(save_path)
        plt.close()
        print(f"グラフを保存しました: {save_path}")

    # 1. 全エネルギー (線グラフ)
    save_single_plot(cpu_df['Time'], cpu_df['Total'], 'CPU', 'black',
                     mn_df['Time'], mn_df['Total'], 'MN-Core', 'red',
                     r'$E_{\mathrm{total}}$ [-]', '0205TotalEnergy_v=3.0.pdf', legend_fontsize,
                     plot_as_points=False)

    # 2. ポテンシャルエネルギー (線グラフに変更)
    save_single_plot(cpu_df['Time'], cpu_df['Potential'], 'CPU', 'darkred',
                     mn_df['Time'], mn_df['Potential'], 'MN-Core', 'black',
                     r'$E_{\mathrm{potential}}$ [-]', '0205PotentialEnergy_v=3.0.pdf', legend_fontsize,
                     plot_as_points=False)

    # 3. 運動エネルギー (線グラフに変更)
    save_single_plot(cpu_df['Time'], cpu_df['Kinetic'], 'CPU', 'blue',
                     mn_df['Time'], mn_df['Kinetic'], 'MN-Core', 'black',
                     r'$E_{\mathrm{kinetic}}$ [-]', '0205KineticEnergy_v=3.0.pdf', legend_fontsize,
                     plot_as_points=False)

if __name__ == "__main__":
    plot_comparison_separate()