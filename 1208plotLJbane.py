import matplotlib.pyplot as plt

def main():
    # データの読み込み
    filename = '1207LJbanedoubleresult.txt'

    energies = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        energies.append(float(line))
                    except ValueError:
                        continue
    except FileNotFoundError:
        print(f"エラー: {filename} が見つかりません。")
        return

    # パラメータ設定
    dt = 0.001  # 時間刻み幅

    # 時間軸の生成
    time_steps = [i * dt for i in range(len(energies))]

    # --- グラフ描画設定 ---
    # 文字サイズを全体的に大きく設定 (ここを調整するとさらに変わります)
    plt.rcParams.update({'font.size': 18})

    plt.figure(figsize=(10, 6))
    
    # プロット
    plt.plot(time_steps, energies, label='Total Energy', color='blue', linewidth=2)

    # ラベルの設定 (タイトルは削除しました)
    plt.xlabel('Time')
    plt.ylabel('Total Energy')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=16) # 凡例のサイズも明示的に指定可能
    plt.tight_layout() # ラベルが見切れないように自動調整

    # --- PNGファイルとして保存 ---
    output_file = 'total_energy_plot.png'
    plt.savefig(output_file, dpi=300) # dpi=300できれいに保存
    print(f"グラフを保存しました: {output_file}")
    
    # plt.show() は削除 (エラー回避のため)

if __name__ == "__main__":
    main()