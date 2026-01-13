import pandas as pd
import matplotlib.pyplot as plt

def main():
    # --- 設定 ---
    input_file = 'mdfree4_cpu_result_float.txt'
    output_file = 'mdfree4_cpu_energy_plot.pdf' # 出力するPDFファイル名
    
    # --- データの読み込み ---
    # 列構成: Time, Potential, Kinetic, Total
    try:
        df = pd.read_csv(input_file, sep='\s+', header=None, 
                         names=['Time', 'Potential', 'Kinetic', 'Total'])
    except Exception as e:
        print(f"エラー: ファイル '{input_file}' を読み込めませんでした。")
        print(e)
        return

    # --- プロット作成 ---
    plt.figure(figsize=(10, 6))
    
    # 3つのエネルギーをプロット
    # ポテンシャルエネルギー (青)
    plt.plot(df['Time'], df['Potential'], label='Potential Energy', color='blue', alpha=0.7, linewidth=1.5)
    
    # 運動エネルギー (緑)
    plt.plot(df['Time'], df['Kinetic'], label='Kinetic Energy', color='green', alpha=0.7, linewidth=1.5)
    
    # 全エネルギー (赤)
    plt.plot(df['Time'], df['Total'], label='Total Energy', color='red', linewidth=2.0)
    
    # --- グラフの装飾 ---
    plt.xlabel('Time [s]')
    plt.ylabel('Energy')
    plt.legend(loc='best') # 凡例を表示
    plt.grid(True)         # グリッドを表示
    
    # タイトルはなし (User request)
    # plt.title(...) 
    
    plt.tight_layout()
    
    # --- 保存 ---
    plt.savefig(output_file)
    print(f"グラフを保存しました: {output_file}")

if __name__ == "__main__":
    main()