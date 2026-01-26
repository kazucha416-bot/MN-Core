import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_combined():
    # ==========================================
    # ★設定パラメータ
    # ==========================================
    legend_fontsize = 14  # 線が多いので少し小さめに調整 (元20だと隠れる可能性あり)
    label_fontsize = 16   # 軸ラベルのフォントサイズ
    tick_fontsize = 16    # 目盛りのフォントサイズ
    
    # 保存先ディレクトリ
    save_dir = r'/home/kazuki/thesis/images'
    os.makedirs(save_dir, exist_ok=True)

    # 保存ファイル名
    output_filename = 'AllEnergies_Combined_Comparison.pdf'

    # 入力ファイル名
    cpu_file = '0113mdfree4_cpu_result_float_3000.txt' 
    mn_core_file = '0113mdfree4_mncore_3000results.txt'

    # --- データの読み込み ---
    try:
        # CPUデータ
        cpu_df = pd.read_csv(cpu_file, sep='\s+', header=None, 
                             names=['Time', 'Potential', 'Kinetic', 'Total'])
        # MN-Coreデータ
        mn_df = pd.read_csv(mn_core_file, sep='\s+', skiprows=2, 
                            names=['Time', 'Potential', 'Kinetic', 'Total'])
        mn_df = mn_df.apply(pd.to_numeric, errors='coerce').dropna()
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return

    # ==========================================
    # プロット作成 (すべてを1枚に)
    # ==========================================
    # 少し横長にして見やすくする
    plt.figure(figsize=(12, 7))
    
    # -------------------------------------------------------
    # 1. Total Energy (全エネルギー)
    # -------------------------------------------------------
    plt.plot(cpu_df['Time'], cpu_df['Total'], label='Total (CPU)', 
             color='black', linestyle='-', linewidth=2.0, alpha=0.8)
    
    plt.plot(mn_df['Time'], mn_df['Total'], label='Total (MN-Core)', 
             color='red', linestyle='--', linewidth=2.5, alpha=0.9)

    # -------------------------------------------------------
    # 2. Potential Energy (ポテンシャルエネルギー)
    # -------------------------------------------------------
    plt.plot(cpu_df['Time'], cpu_df['Potential'], label='Potential (CPU)', 
             color='blue', linestyle='-', linewidth=1.5, alpha=0.6)
    
    plt.plot(mn_df['Time'], mn_df['Potential'], label='Potential (MN-Core)', 
             color='orange', linestyle='--', linewidth=2.0, alpha=0.8)

    # -------------------------------------------------------
    # 3. Kinetic Energy (運動エネルギー)
    # -------------------------------------------------------
    plt.plot(cpu_df['Time'], cpu_df['Kinetic'], label='Kinetic (CPU)', 
             color='green', linestyle='-', linewidth=1.5, alpha=0.6)
    
    plt.plot(mn_df['Time'], mn_df['Kinetic'], label='Kinetic (MN-Core)', 
             color='purple', linestyle='--', linewidth=2.0, alpha=0.8)


    # --- レイアウト設定 ---
    plt.xlabel('Time [-]', fontsize=label_fontsize)
    # Y軸ラベルはすべてを代表して「Energy」とする
    plt.ylabel('Energy [-]', fontsize=label_fontsize)
    
    plt.tick_params(labelsize=tick_fontsize)
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # 凡例の設定 (ncol=2 で2列にして高さを抑える)
    plt.legend(loc='best', fontsize=legend_fontsize, ncol=2)
    
    plt.tight_layout()
    
    # 保存
    save_path = os.path.join(save_dir, output_filename)
    plt.savefig(save_path)
    plt.close()
    print(f"グラフを保存しました: {save_path}")

if __name__ == "__main__":
    plot_combined()