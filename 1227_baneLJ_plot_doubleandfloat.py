import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import struct
import os

def main():
    # --- 設定 ---
    file_double = '1227baneljdouble_result.txt'
    file_float  = '1227baneljfloat_result.txt'
    output_filename = '1227_banelj_comparison_solid.pdf' # ファイル名も少し変えました
    save_dir = r'/home/kazuki/thesis/images'
    # シミュレーション設定
    dt = 0.001
    total_steps = 2000
    
    # 時間軸: Step 1, 10, 20... 2000 (計201点)
    steps = [1] + list(range(10, total_steps + 1, 10))
    time_axis = np.array(steps) * dt

    # --- 関数定義 ---
    
    # 倍精度 (64bit Hex -> Double)
    def hex_to_double(hex_str):
        s = hex_str.strip().replace('0x', '').replace(',', '')
        s = s.zfill(16)
        try:
            return struct.unpack('>d', bytes.fromhex(s))[0]
        except ValueError:
            return None

    # 単精度 (Hex -> Float)
    def hex_to_float(hex_str):
        s = hex_str.strip().replace('0x', '').replace(',', '')
        # 16桁なら上位8桁を採用、それ以下なら8桁ゼロ埋め
        if len(s) > 8:
            s = s[:8]
        s = s.zfill(8)
        try:
            return struct.unpack('>f', bytes.fromhex(s))[0]
        except ValueError:
            return None

    # --- データ読み込み関数 ---
    def load_data(filename, parser_func):
        if not os.path.exists(filename):
            print(f"エラー: ファイル '{filename}' が見つかりません。")
            return None
        
        vals = []
        with open(filename, 'r') as f:
            content = f.read().replace(',', ' ')
            tokens = content.split()
            for token in tokens:
                val = parser_func(token)
                if val is not None:
                    vals.append(val)
        return np.array(vals)

    # --- メイン処理 ---
    print("データを読み込んでいます...")
    e_double = load_data(file_double, hex_to_double)
    e_float  = load_data(file_float, hex_to_float)

    # データ整合性チェックと切り詰め
    min_len = len(time_axis)
    if e_double is not None: min_len = min(min_len, len(e_double))
    if e_float is not None:  min_len = min(min_len, len(e_float))
    
    t_plot = time_axis[:min_len]
    if e_double is not None: e_double = e_double[:min_len]
    if e_float is not None:  e_float  = e_float[:min_len]

    # --- 統計量計算 (コンソール出力) ---
    print("\n" + "="*65)
    print(f"{'Type':<10} | {'Initial E':<15} | {'Final E':<15} | {'Drift (%)'}")
    print("="*65)
    if e_double is not None:
        drift_d = (e_double[-1] - e_double[0]) / e_double[0] * 100
        print(f"{'Double':<10} | {e_double[0]:.8f} | {e_double[-1]:.8f} | {drift_d:+.4e} %")
    if e_float is not None:
        drift_f = (e_float[-1] - e_float[0]) / e_float[0] * 100
        print(f"{'Float':<10} | {e_float[0]:.8f} | {e_float[-1]:.8f} | {drift_f:+.4e} %")
    print("="*65 + "\n")

    # --- プロット処理 ---
    plt.rcParams.update({'font.size': 18})
    plt.figure(figsize=(12, 8))
    
    # 1. 倍精度 (赤・実線)
    if e_double is not None:
        plt.plot(t_plot, e_double, label='MN-Core 2 (Double)', 
                 color='tab:red', linestyle='-', linewidth=2.5, alpha=0.9)

    # 2. 単精度 (青・実線) ★ここを変更しました
    if e_float is not None:
        plt.plot(t_plot, e_float, label='MN-Core 2 (Float)', 
                 color='tab:blue', linestyle='-', linewidth=2.5, alpha=0.9)

    # 装飾
    plt.xlabel('Time [s]', fontsize=24)
    plt.ylabel('Total Energy', fontsize=24)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=False, fontsize=20, loc='best')
    plt.xlim(0, 2.0)
    
    # Y軸: オフセット無効化
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    plt.gca().yaxis.set_major_formatter(y_formatter)

    plt.tight_layout()

    # 保存
    plt.savefig(os.path.join(save_dir, output_filename), dpi=300)
    print(f"比較グラフ(両方実線)を保存しました: {output_filename}")

if __name__ == "__main__":
    main()