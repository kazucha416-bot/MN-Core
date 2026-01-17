import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import os

def run_simulation_and_plot():
    # --- 1. Cコードのコンパイル ---
    c_source = "md_pbc.c"     # ソースコード名
    executable = "md_pbc"     # 生成する実行ファイル名
    
    print(f"🔨 Compiling {c_source}...")
    # gcc md_pbc.c -o md_pbc -lm を実行
    try:
        subprocess.run(["gcc", c_source, "-o", executable, "-lm"], check=True)
    except subprocess.CalledProcessError:
        print("❌ コンパイルエラー！コードを確認してください。")
        return

    # --- 2. Cプログラムの実行 ---
    print(f"🚀 Running simulation...")
    try:
        subprocess.run([f"./{executable}"], check=True)
    except subprocess.CalledProcessError:
        print("❌ 実行時エラー！")
        return

    # --- 3. Pythonでプロット (さっきのコードと同じ) ---
    print(f"📈 Plotting results...")
    
    filename = 'MD_PBC_RDF.txt'
    if not os.path.exists(filename):
        print(f"エラー: データファイル {filename} が見つかりません。")
        return

    try:
        df = pd.read_csv(filename, sep='\s+', header=None, names=['r', 'g_r'])
        
        plt.figure(figsize=(8, 6))
        plt.plot(df['r'], df['g_r'], color='red', linewidth=2, label='RDF $g(r)$')
        plt.axhline(1.0, color='gray', linestyle='--', linewidth=1, label='Ideal Gas')
        plt.xlabel('Distance $r$', fontsize=14)
        plt.ylabel('$g(r)$', fontsize=14)
        plt.title('Radial Distribution Function', fontsize=16)
        plt.xlim(0, df['r'].max())
        plt.ylim(0, df['g_r'].max() * 1.1)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        
        # 保存して表示
        plt.savefig("RDF_result.pdf")
        print("✅ 完了！グラフを保存しました: RDF_result.pdf")
        # 環境によっては以下でウィンドウが開きます
        # plt.show() 
        
    except Exception as e:
        print(f"プロット中にエラーが発生しました: {e}")

if __name__ == "__main__":
    run_simulation_and_plot()