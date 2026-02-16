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
    mn_core_file = '0216_freemd4_decimal.txt'

    # --- データの読み込み ---
    try:
        # MN-Coreのデータのみ読み込み
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
        plt.plot(x, y, label=label, color=color, 
                 linestyle='-', linewidth=2.0, alpha=0.8)
        
        # ラベル設定
        plt.xlabel('Time [-]', fontsize=label_fontsize)
        plt.ylabel(ylabel, fontsize=label_fontsize)
        
        # 軸の数字（目盛り）の設定
        plt.tick_params(labelsize=tick_fontsize)
        
        # ===========================================================
        # ★ここを追加: オフセット表示を無効化 (値をそのまま表示)
        # ===========================================================
        # useOffset=False: +2.5e3 のようなオフセット表記を禁止
        # axis='y': Y軸のみ適用
        plt.ticklabel_format(useOffset=False, axis='y')
        
        # ※もし「1e-5」のような指数表記(x10^n)もやめたい場合は、
        #   style='plain' を追加してください。
        # plt.ticklabel_format(useOffset=False, style='plain', axis='y')

        # 凡例
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
                     r'$E_{\mathrm{total}}$ [-]', '0216TotalEnergy_v=0.5~1.0_MN.pdf')

    # 2. ポテンシャルエネルギー (濃い青)
    save_single_plot(mn_df['Time'], mn_df['Potential'], 'MN-Core', 'darkblue',
                     r'$E_{\mathrm{potential}}$ [-]', '0216PotentialEnergy_v=0.5~1.0_MN.pdf')

    # 3. 運動エネルギー (赤)
    save_single_plot(mn_df['Time'], mn_df['Kinetic'], 'MN-Core', 'red',
                     r'$E_{\mathrm{kinetic}}$ [-]', '0216KineticEnergy_v=0.5~1.0_MN.pdf')

if __name__ == "__main__":
    plot_mncore_only()