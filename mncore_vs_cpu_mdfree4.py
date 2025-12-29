import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

def main():
    # --- 設定 ---
    mn_file = 'mdfree4_mncore_result.txt'
    cpu_file = 'mdfree4_cpu_result.txt'
    output_filename = 'compare_mncore_cpu.pdf'

    # --- データ読み込み関数 ---
    def load_data(filename, label):
        if not os.path.exists(filename):
            print(f"エラー: {filename} が見つかりません。")
            return None, None
        
        try:
            # comment='-' を削除しました（負の数が消えないように）
            # ヘッダーなしとして読み込み、あとで非数値行を除外します
            df = pd.read_csv(filename, sep=r'\s+', header=None)
            
            # 0列目（時間）が数値に変換できる行だけを残すフィルタリング
            # これでヘッダー行("Time...")や区切り線("----")は自動的に消えます
            df = df[pd.to_numeric(df[0], errors='coerce').notnull()]
            
            # 型変換
            t = df.iloc[:, 0].astype(float)
            e = df.iloc[:, 3].astype(float) # 4列目(Total Energy)
            
            return t, e
        except Exception as e:
            print(f"{label} 読み込みエラー: {e}")
            # エラー時のデータの中身を確認しやすくするデバッグ表示
            try:
                print("  (読み込んだデータの先頭5行:)")
                print(df.head())
            except:
                pass
            return None, None

    # --- メイン処理 ---
    print("データを読み込んでいます...")
    t_mn, e_mn = load_data(mn_file, "MN-Core")
    t_cpu, e_cpu = load_data(cpu_file, "CPU")

    if t_mn is None or t_cpu is None:
        print("データの読み込みに失敗したため、プロットを中止します。")
        return

    print(f"MN-Core Data: {len(t_mn)} points")
    print(f"CPU Data    : {len(t_cpu)} points")

    # --- プロット ---
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(10, 6))

    # CPU (正解データ) - 黒実線
    plt.plot(t_cpu, e_cpu, label='CPU (Double)', color='black', linewidth=2.0, alpha=0.8)
    
    # MN-Core (検証データ) - 赤破線
    # ※データ点数が多いので少し間引くか、透過度を上げて見やすく
    plt.plot(t_mn, e_mn, label='MN-Core (Float)', color='tab:red', linestyle='--', linewidth=2.5, alpha=0.9)

    plt.xlabel('Time [s]', fontsize=20)
    plt.ylabel('Total Energy', fontsize=20)
    plt.legend(fontsize=16)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # 軸の範囲調整 (短い方のデータの終了時間に合わせる)
    t_max = min(t_mn.max(), t_cpu.max())
    plt.xlim(0, t_max) 
    
    # Y軸: オフセットなし
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print(f"比較グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    main()