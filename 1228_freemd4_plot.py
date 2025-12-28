import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct
import os

def main():
    # --- 設定 ---
    input_filename = 'freemd4result.txt'
    output_filename = '4particle_total_energy_only.pdf'
    
    # データ構造の設定
    n_steps = 10
    n_ke_per_step = 4
    n_pe_per_step = 16

    # --- 関数定義 ---
    def hex_to_float(hex_str):
        s = hex_str.strip().replace('0x', '').replace(',', '')
        if len(s) > 8: s = s[:8]
        s = s.zfill(8)
        try:
            return struct.unpack('>f', bytes.fromhex(s))[0]
        except ValueError:
            return 0.0

    # --- データ読み込み ---
    if not os.path.exists(input_filename):
        print(f"エラー: ファイル '{input_filename}' が見つかりません。")
        return

    raw_data = []
    with open(input_filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            raw_data.append(hex_to_float(line))
    
    raw_data = np.array(raw_data)
    
    # データ数チェック
    expected_len = n_steps * (n_ke_per_step + n_pe_per_step)
    if len(raw_data) < expected_len:
        print(f"警告: データ不足 (現在: {len(raw_data)}, 想定: {expected_len})")
        n_steps = len(raw_data) // (n_ke_per_step + n_pe_per_step)

    # --- エネルギー計算 ---
    ke_list = []
    pe_list = []
    
    # 分割
    ke_raw_part = raw_data[: n_steps * n_ke_per_step]
    pe_raw_part = raw_data[n_steps * n_ke_per_step : n_steps * (n_ke_per_step + n_pe_per_step)]

    # KE計算
    for i in range(n_steps):
        block = ke_raw_part[i*4 : (i+1)*4]
        ke_list.append(np.sum(block))

    # PE計算
    for i in range(n_steps):
        block = pe_raw_part[i*16 : (i+1)*16]
        # 後半4つのinf無視、和を半分にする
        valid_block = block[:-4]
        pe_list.append(np.sum(valid_block) / 2.0)

    # 合計エネルギー
    total_energy = np.array(ke_list) + np.array(pe_list)
    steps_axis = np.arange(1, n_steps + 1)

    # --- コンソール出力 (確認用) ---
    print(f"{'Step':<5} | {'Total Energy':<15}")
    print("-" * 25)
    for i in range(n_steps):
        print(f"{i+1:<5} | {total_energy[i]:.8f}")
    
    drift = (total_energy[-1] - total_energy[0]) / total_energy[0] * 100
    print("-" * 25)
    print(f"Drift: {drift:+.4e} %")

    # --- プロット処理 ---
    plt.rcParams.update({'font.size': 16})
    plt.figure(figsize=(10, 6))

    # Total Energyのみプロット (赤・実線・マーカーあり)
    plt.plot(steps_axis, total_energy, label='Total Energy', 
             marker='o', markersize=8, linewidth=2.5, color='tab:red')

    plt.xlabel('Step')
    plt.ylabel('Total Energy')
    # タイトル削除（論文用など汎用的に）
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(steps_axis) # 整数ステップを表示

    # ★重要: Y軸のオフセット表記を無効化し、そのままの数値を表示
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    plt.gca().yaxis.set_major_formatter(y_formatter)

    plt.tight_layout()
    plt.savefig(output_filename)
    print(f"グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    main()