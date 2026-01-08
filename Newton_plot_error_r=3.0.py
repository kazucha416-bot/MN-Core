import struct
import matplotlib.pyplot as plt
import os

def hex_to_double(hex_str):
    """16進数文字列(64bit)を倍精度浮動小数点数に変換"""
    hex_str = hex_str.strip().replace('0x', '')
    int_val = int(hex_str, 16)
    return struct.unpack('>d', struct.pack('>Q', int_val))[0]

def hex_to_float(hex_str):
    """16進数文字列(32bit)を単精度浮動小数点数に変換"""
    hex_str = hex_str.strip().replace('0x', '')
    int_val = int(hex_str, 16)
    return struct.unpack('>f', struct.pack('>I', int_val))[0]

def main():
    # --- データ定義 ---
    # r = 3.0
    r = 3.0
    actual_val = 1.0 / (r ** 0.5)  # 真値 (倍精度)
    
    # 倍精度データ
    data_points_double = [
        (0, "3fe2000000000000"),
        (1, "3fe2750000000000"),
        (2, "3fe279a583a32000"),
        (3, "3fe279a7458ff2e9"),
        (4, "3fe279a74590331c"),
        (5, "3fe279a74590331c"),
    ]

    # 単精度データ
    data_points_single = [
        (0, "0x3f100000"),
        (1, "0x3f13a800"),
        (2, "0x3f13cd2d"),
        (3, "0x3f13cd3b"),
        (4, "0x3f13cd3a"),
        (5, "0x3f13cd3a"),
    ]

    # --- 計算処理 ---
    iters_d, errors_d = [], []
    iters_s, errors_s = [], []
    
    eps_double = 1e-16
    eps_single = 1e-9

    # 倍精度の誤差計算
    for i, hex_str in data_points_double:
        val = hex_to_double(hex_str)
        error = abs(val - actual_val)
        if error == 0.0: error = eps_double
        iters_d.append(i)
        errors_d.append(error)

    # 単精度の誤差計算
    for i, hex_str in data_points_single:
        val = hex_to_float(hex_str)
        error = abs(val - actual_val)
        if error == 0.0: error = eps_single
        iters_s.append(i)
        errors_s.append(error)

    # --- グラフ描画設定 ---
    plt.rcParams.update({'font.size': 20})
    plt.figure(figsize=(10, 6))
    
    # Double Precision (Navy)
    plt.plot(iters_d, errors_d, marker='o', linestyle='-', color='navy', 
             label='Double Precision', markersize=10, linewidth=2.5)

    # Single Precision (Red)
    plt.plot(iters_s, errors_s, marker='s', linestyle='--', color='tab:red', 
             label='Single Precision', markersize=10, linewidth=2.5)
    
    plt.yscale('log')
    plt.xlabel('Number of Iterations', fontsize=18)
    plt.ylabel('Absolute Error', fontsize=18)
    
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.xticks(iters_d)
    plt.legend(fontsize=16)
    
    plt.tight_layout()
    
    # --- 保存処理 ---
    save_dir = r'/home/kazuki/thesis/images'  
    filename = 'newton_r=3.0.pdf'
    
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    plt.savefig(save_path, dpi=300)
    print(f"Graph saved as {save_path}")

if __name__ == "__main__":
    main()