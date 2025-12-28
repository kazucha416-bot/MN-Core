import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

def main():
    # --- 設定 ---
    input_filename = '1228_energy_log.txt'
    output_filename = 'MN-Core 2_Freemd4.pdf'

    # --- データ読み込み ---
    if not os.path.exists(input_filename):
        print(f"エラー: '{input_filename}' が見つかりません。")
        print("いただいたデータをコピーして、この名前で保存してください。")
        return

    # 空白またはタブ区切りとして読み込み
    try:
        df = pd.read_csv(input_filename, sep='\s+', header=None)
        # 0列目: Time, 3列目: Total Energy
        time_data = df.iloc[:, 0]
        total_energy = df.iloc[:, 3]
    except Exception as e:
        print(f"読み込みエラー: {e}")
        return

    # --- プロット処理 ---
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(10, 6))

    # Total Energy (黒の実線)
    plt.plot(time_data, total_energy, label='Total Energy (C Reference)', 
             color='black', linewidth=1.5, alpha=0.9)

    # 装飾
    plt.xlabel('Time', fontsize=20)
    plt.ylabel('Total Energy', fontsize=20)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=False, fontsize=16)

    # Y軸: オフセット無効化 (微小な変動を見るため必須)
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    plt.gca().yaxis.set_major_formatter(y_formatter)
    
    # 軸の範囲を少し調整して見やすく
    plt.xlim(time_data.min(), time_data.max())

    plt.tight_layout()

    # 保存
    plt.savefig(output_filename, dpi=300)
    print(f"グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    main()