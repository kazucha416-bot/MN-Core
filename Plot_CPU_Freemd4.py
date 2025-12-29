import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

def main():
    # --- 設定 ---
    input_filename = 'mdfree4_cpu_result.txt'
    output_filename = 'CPU_Freemd4.pdf'

    # --- データ読み込み ---
    if not os.path.exists(input_filename):
        print(f"エラー: ファイル '{input_filename}' が見つかりません。")
        return

    try:
        # 空白区切りで読み込み
        # 列: 0:Time, 1:PE, 2:KE, 3:TotalE (4列目)
        df = pd.read_csv(input_filename, sep=r'\s+', header=None, comment='#')
        
        time_data = df.iloc[:, 0]
        total_energy = df.iloc[:, 3] # 4列目を取得

    except Exception as e:
        print(f"読み込みエラー: {e}")
        return

    # --- 統計量表示 (確認用) ---
    e0 = total_energy.iloc[0]
    e_last = total_energy.iloc[-1]
    drift = (e_last - e0) / abs(e0) * 100
    
    print("-" * 40)
    print(f"Data Points    : {len(df)}")
    print(f"Initial Energy : {e0:.8f}")
    print(f"Final Energy   : {e_last:.8f}")
    print(f"Energy Drift   : {drift:+.4e} %")
    print("-" * 40)

    # --- プロット処理 ---
    plt.rcParams.update({'font.size': 18}) # 基本フォントサイズ
    fig = plt.figure(figsize=(10, 6))
    
    # 余白調整 [left, bottom, width, height]
    # ラベルが切れないように左と下を確保
    ax = fig.add_axes([0.18, 0.15, 0.78, 0.80])

    # プロット (黒の実線)
    ax.plot(time_data, total_energy, label='Total Energy (CPU)', 
             color='black', linewidth=2.0, alpha=0.9)

    # 軸ラベル
    ax.set_xlabel('Time [s]', fontsize=24)
    ax.set_ylabel('Total Energy', fontsize=24)
    
    # 目盛りサイズ
    ax.tick_params(axis='both', labelsize=18)
    
    # グリッド
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # 凡例 (枠なし)
    ax.legend(frameon=False, fontsize=18, loc='best')

    # Y軸: オフセット表記を無効化 (数値をそのまま表示)
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(y_formatter)
    
    # X軸の範囲をデータに合わせる
    ax.set_xlim(time_data.min(), time_data.max())

    # --- 保存 ---
    plt.savefig(output_filename, dpi=300)
    print(f"グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    main()