# 卒論訂正のために，初期速度を調整したものをCPUとMN-Coreで比較するコード．
# CPUとMN-Coreの両方のデータを読み込んで、同じグラフにプロットするスクリプト
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_comparison_separate():
    # ==========================================
    # ★設定パラメータ
    # ==========================================
    # 保存先ファイル名とディレクトリ
    save_dir = r'/home/kazuki/thesis/images/'
    os.makedirs(save_dir, exist_ok=True)
    
    # 読み込むファイル名
    cpu_file = '0216_mdfree4_cpu.txt' 
    mn_core_file = '0216_freemd4_decimal.txt'

    # フォントサイズ
    label_fontsize = 16
    tick_fontsize = 14
    legend_fontsize = 14

    # ==========================================
    # データの読み込み
    # ==========================================
    try:
        # 1. CPUデータの読み込み (ヘッダーなし)
        # 列: 0=Time, 1=Potential, 2=Kinetic, 3=Total
        df_cpu = pd.read_csv(cpu_file, sep=r'\s+', header=None, 
                             names=['Time', 'Potential', 'Kinetic', 'Total'])
        
        # 2. MN-Coreデータの読み込み (ヘッダーあり、2行スキップ)
        df_mn = pd.read_csv(mn_core_file, sep=r'\s+', skiprows=2, 
                            names=['Time', 'Potential', 'Kinetic', 'Total'])
        
        # 数値化と欠損値の除去
        df_mn = df_mn.apply(pd.to_numeric, errors='coerce').dropna()
        
        print(f"データ読み込み完了: CPU({len(df_cpu)}行), MN-Core({len(df_mn)}行)")

    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # ==========================================
    # 共通プロット関数
    # ==========================================
    def create_plot(col_name, ylabel, output_filename):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # CPUプロット (黒・実線)
        ax.plot(df_cpu['Time'], df_cpu[col_name], label='CPU', 
                color='black', linestyle='-', linewidth=2.0, alpha=0.7)
        
        # MN-Coreプロット (赤・破線)
        ax.plot(df_mn['Time'], df_mn[col_name], label='MN-Core 2', 
                color='red', linestyle='--', linewidth=2.0, alpha=0.8)
        
        # 軸ラベル設定
        ax.set_xlabel('Time [-]', fontsize=label_fontsize)
        ax.set_ylabel(ylabel, fontsize=label_fontsize)
        
        # 目盛りの設定
        ax.tick_params(axis='both', labelsize=tick_fontsize)
        
        # ★重要: オフセット表記を無効化 (例: +2.5e3 を表示しない)
        ax.ticklabel_format(useOffset=False, axis='y')
        
        # グリッドと凡例
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='best', fontsize=legend_fontsize, frameon=False)
        
        # 保存
        plt.tight_layout()
        save_path = os.path.join(save_dir, output_filename)
        plt.savefig(save_path)
        plt.close()
        print(f"グラフを作成しました: {save_path}")

    # ==========================================
    # グラフ作成実行
    # ==========================================
    
    # 1. トータルエナジー
    create_plot('Total', r'$E_{\mathrm{total}}$ [-]', '0216Comparison_TotalEnergy.pdf')

    # 2. 運動エネルギー
    create_plot('Kinetic', r'$E_{\mathrm{kinetic}}$ [-]', '0216Comparison_KineticEnergy.pdf')

    # 3. ポテンシャルエネルギー
    create_plot('Potential', r'$E_{\mathrm{potential}}$ [-]', '0216Comparison_PotentialEnergy.pdf')

if __name__ == "__main__":
    plot_comparison_separate()