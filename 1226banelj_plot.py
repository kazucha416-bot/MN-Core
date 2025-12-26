import matplotlib.pyplot as plt
import numpy as np
import os
import struct

def main():
    # --- 設定 ---
    # 入力ファイル名
    file_float = '1226baneljfloatresult.txt'
    file_double = '1226baneljdoubleresult.txt'
    
    # 保存先のディレクトリとファイル名
    save_dir = r'/home/kazuki/thesis/images' 
    filename = '1226banelj.pdf'  
    save_path = os.path.join(save_dir, filename)

    # シミュレーション設定
    dt = 0.001

    # --- 16進数変換関数 ---
    def hex_to_float(s):
        s = s.strip().replace('0x', '').replace(',', '')
        try:
            return struct.unpack('>f', bytes.fromhex(s))[0]
        except ValueError:
            return None

    def hex_to_double(s):
        s = s.strip().replace('0x', '').replace(',', '')
        try:
            return struct.unpack('>d', bytes.fromhex(s))[0]
        except ValueError:
            return None

    # --- データ読み込み ---
    def load_data(filename, mode='float'):
        if not os.path.exists(filename):
            print(f"⚠️ ファイルが見つかりません: {filename}")
            return None
        
        vals = []
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.strip(): continue
                if mode == 'float':
                    val = hex_to_float(line)
                else:
                    val = hex_to_double(line)
                if val is not None:
                    vals.append(val)
        return np.array(vals)

    print("データを読み込んでいます...")
    data_float = load_data(file_float, mode='float')
    data_double = load_data(file_double, mode='double')

    # --- プロット設定 ---
    plt.rcParams.update({'font.size': 24})
    plt.rcParams['axes.linewidth'] = 2.0
    plt.rcParams['xtick.major.width'] = 2.5
    plt.rcParams['ytick.major.width'] = 2.5
    plt.rcParams['xtick.major.size'] = 10
    plt.rcParams['ytick.major.size'] = 10

    plt.figure(figsize=(12, 8))
    plt.subplots_adjust(left=0.18, bottom=0.15, right=0.95, top=0.95)

    # --- 描画 (実線) ---
    if data_float is not None:
        time_axis = np.arange(len(data_float)) * dt
        plt.plot(time_axis, data_float, label='Single Precision', 
                 color='tab:blue', linestyle='-', linewidth=2.5, alpha=0.8)

    if data_double is not None:
        time_axis = np.arange(len(data_double)) * dt
        plt.plot(time_axis, data_double, label='Double Precision', 
                 color='tab:red', linestyle='-', linewidth=2.5, alpha=0.8)

    plt.xlabel('Time [s]', fontsize=28)
    plt.ylabel('Total Energy', fontsize=28)
    plt.xlim(0, 2.0)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(frameon=False, loc='best', fontsize=22)

    # --- ★保存実行はここ！（全ての描画が終わった後）---
    # ディレクトリの存在確認（なければ作る設定にしていますが、あるならスルーされます）
    os.makedirs(save_dir, exist_ok=True)
    
    plt.savefig(save_path, dpi=300)
    print(f"Graph saved as {save_path}")

if __name__ == "__main__":
    main()