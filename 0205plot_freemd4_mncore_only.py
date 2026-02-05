import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_mncore_only():
    # ==========================================
    # ★設定パラメータ
    # ==========================================
    legend_fontsize = 20  # 凡例のフォントサイズ
    label_fontsize = 16   # 軸ラベルのフォントサイズ
    tick_fontsize = 16    # 軸の数字のフォントサイズ
    
    # --- 保存先ディレクトリの設定 ---
    save_dir = r'/home/kazuki/thesis/images/'
    os.makedirs(save_dir, exist_ok=True)

    # --- 読み込むファイル名 ---
    # CPUのファイル設定は削除しました
    mn_core_file = '0205_freemd4_v=0.5~1.0_decimal.txt'

    # --- データの読み込み ---
    try:
        # MN-Coreのデータのみ読み込み
        # sep=r'\s+', skiprows=2 はそのまま維持
        mn_df = pd.read_csv(mn_core_file, sep=r'\s+', skiprows=2, 
                            names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = mn_df.apply(pd.to_numeric, errors='coerce').dropna()
        print(f"データを読み込みました: {mn_core_file}")
        
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # --- プロット関数 (1データセット用) ---
    def save_single_plot(x, y, label, color, ylabel, filename):
        
        # 図のサイズ設定
        plt.figure(figsize=(10, 6))
        
        # プロット (線モード)
        # 比較ではないので、実線で見やすく描画します
        plt.plot(x, y, label=label, color=color, 
                 linestyle='-', linewidth=2.0, alpha=0.8)
        
        # ラベル設定
        plt.xlabel('Time [-]', fontsize=label_fontsize)
        plt.ylabel(ylabel, fontsize=label_fontsize)
        
        # 軸の数字（目盛り）の設定
        plt.tick_params(labelsize=tick_fontsize)
        
        # 凡例
        # データが1つだけなので、凡例は必須ではありませんが、
        # "MN-Core" であることを示すために残しておきます
        plt.legend(bbox_to_anchor=(0.5, 1.05), loc='lower center', borderaxespad=0, 
                   fontsize=16, frameon=False)
        
        plt.grid(True)
        plt.tight_layout()
        
        # 保存
        save_path = os.path.join(save_dir, filename)
        plt.savefig(save_path)
        plt.close()
        print(f"グラフを保存しました: {save_path}")

    # ==========================================
    # ★グラフ作成実行
    # ==========================================
    
    # 1. 全エネルギー (黒)
    save_single_plot(mn_df['Time'], mn_df['Total'], 'MN-Core', 'black',
                     r'$E_{\mathrm{total}}$ [-]', '0205TotalEnergy_v=0.5~1.0_MN.pdf')

    # 2. ポテンシャルエネルギー (濃い青)
    save_single_plot(mn_df['Time'], mn_df['Potential'], 'MN-Core', 'darkblue',
                     r'$E_{\mathrm{potential}}$ [-]', '0205PotentialEnergy_v=0.5~1.0_MN.pdf')

    # 3. 運動エネルギー (赤)
    save_single_plot(mn_df['Time'], mn_df['Kinetic'], 'MN-Core', 'red',
                     r'$E_{\mathrm{kinetic}}$ [-]', '0205KineticEnergy_v=0.5~1.0_MN.pdf')

if __name__ == "__main__":
    plot_mncore_only()