import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_rdf():
    # --- 設定 ---
    # 読み込むファイル名（C言語で出力したファイル名に合わせてください）
    filename = 'MD_PBC_RDF.txt'
    # 保存する画像ファイル名
    output_pdf = 'MD_PBC_RDF_plot.pdf'

    # --- データの読み込み ---
    # ヘッダーがない空白区切りのデータを想定
    try:
        df = pd.read_csv(filename, sep='\s+', header=None, names=['r', 'g_r'])
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        print(f"※ '{filename}' が同じフォルダにあるか確認してください。")
        return

    # --- プロット ---
    plt.figure(figsize=(8, 6))
    
    # 折れ線グラフ（データ点が多いので線だけでOK）
    plt.plot(df['r'], df['g_r'], color='red', linewidth=2, label='RDF $g(r)$')
    
    # 理想気体（g(r)=1）のライン
    plt.axhline(1.0, color='gray', linestyle='--', linewidth=1, label='Ideal Gas ($g(r)=1$)')

    # --- グラフの装飾 ---
    plt.xlabel('Distance $r$', fontsize=14)
    plt.ylabel('Radial Distribution Function $g(r)$', fontsize=14)
    plt.title('Radial Distribution Function (Liquid $\\rho \\approx 0.5$)', fontsize=16)
    
    # 範囲設定 (データの最大値に合わせて調整)
    plt.xlim(0, df['r'].max())
    plt.ylim(0, df['g_r'].max() * 1.1) # ピークの上少し余裕を持たせる
    
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=12)
    plt.tight_layout()

    # --- 保存 ---
    plt.savefig(output_pdf)
    print(f"グラフを保存しました: {output_pdf}")
    
    # 画面表示（環境によっては表示されないのでsavefig推奨）
    # plt.show()

if __name__ == "__main__":
    plot_rdf()