import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_total_energy():
    # --- 設定 ---
    filename = 'mdfree4_cpu_manual_v.txt'  # 指定されたファイル名
    output_filename = 'TotalEnergy_manual_v.pdf' # PDF形式で保存
    
    # フォントサイズ設定
    label_fontsize = 16
    tick_fontsize = 14
    legend_fontsize = 14

    # --- データの読み込み ---
    if not os.path.exists(filename):
        print(f"エラー: '{filename}' が見つかりません。")
        return

    try:
        # 空白またはタブ区切りで読み込み
        df = pd.read_csv(filename, sep=r'\s+', header=None, 
                         names=['Time', 'Potential', 'Kinetic', 'Total'])
        print(f"データを読み込みました: {len(df)} 行")
    except Exception as e:
        print(f"読み込みエラー: {e}")
        return

    # --- プロット ---
    fig, ax = plt.subplots(figsize=(10, 6))

    # トータルエナジーのみプロット (黒)
    ax.plot(df['Time'], df['Total'], label='Total Energy', color='black', 
            linewidth=2.0, linestyle='-')

    # --- 見た目の調整 ---
    ax.set_xlabel('Time [-]', fontsize=label_fontsize)
    # 軸ラベルを数式表記に
    ax.set_ylabel(r'$E_{\mathrm{total}}$ [-]', fontsize=label_fontsize)
    
    # 目盛りの文字サイズ
    ax.tick_params(axis='both', labelsize=tick_fontsize)

    # ★重要: Y軸のオフセット表示（+2.5e3のような表記）を無効化
    ax.ticklabel_format(useOffset=False, axis='y')

    # グリッド
    ax.grid(True, linestyle='--', alpha=0.6)

    # 凡例 (グラフの上に見やすく配置)
    ax.legend(bbox_to_anchor=(0.5, 1.02), loc='lower center', 
              borderaxespad=0, fontsize=legend_fontsize, frameon=False)

    # レイアウト調整と保存
    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    plot_total_energy()