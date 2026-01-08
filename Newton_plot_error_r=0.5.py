import struct
import matplotlib.pyplot as plt
import os

def hex_to_double(hex_str):
    """16進数文字列(64bit)を倍精度浮動小数点数に変換"""
    s = hex_str.strip().replace('0x', '')
    int_val = int(s, 16)
    return struct.unpack('>d', struct.pack('>Q', int_val))[0]

def hex_to_float(hex_str):
    """16進数文字列(32bit)を単精度浮動小数点数に変換"""
    s = hex_str.strip().replace('0x', '')
    int_val = int(s, 16)
    return struct.unpack('>f', struct.pack('>I', int_val))[0]

def main():
    # --- データ定義 ---
    # r = 0.5 の平方根の逆数を求める
    r = 0.5
    actual_val = 1.0 / (r ** 0.5)  # 真値 (倍精度)
    
    # 倍精度データ (Double)
    data_points_double = [
        (0, "3ff6800000000000"), # drsqrt
        (1, "3ff6a05800000000"), # 1st Newton
        (2, "3ff6a09e6536af66"), # 2nd Newton
        (3, "3ff6a09e667f3bcd"), # 3rd Newton
        (4, "3ff6a09e667f3bcc"), # 4th Newton
        (5, "3ff6a09e667f3bcc"), # 5th Newton
    ]

    # 単精度データ (Single)
    data_points_single = [
        (0, "0x3fb40000"),
        (1, "0x3fb502c0"),
        (2, "0x3fb504f3"),
        (3, "0x3fb504f3"),
        (4, "0x3fb504f3"),
        (5, "0x3fb504f3"),
    ]

    # --- 計算処理 ---
    iters_d, errors_d = [], []
    iters_s, errors_s = [], []
    
    # グラフ描画用に、誤差0になった時の代替値を設定
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
    
    # Double Precision (Navy, Circle, Solid)
    plt.plot(iters_d, errors_d, marker='o', linestyle='-', color='navy', 
             label='Double Precision', markersize=10, linewidth=2.5)

    # Single Precision (Red, Square, Dashed)
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
    filename = 'newton_r=0.5.pdf' 
    
    # ディレクトリ作成
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    plt.savefig(save_path, dpi=300)
    print(f"Graph saved as {save_path}")

if __name__ == "__main__":
    main()