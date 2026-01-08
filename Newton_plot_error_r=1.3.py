import struct
import matplotlib.pyplot as plt
import os

def hex_to_double(hex_str):
    """16進数文字列(64bit)を倍精度浮動小数点数に変換"""
    # 0xを取り除く処理を追加して堅牢に
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
    r = 1.3
    actual_val = 1.0 / (r ** 0.5)  # 1.3の平方根の逆数の真値 (倍精度)
    
    # 倍精度データ (Double)
    data_points_double = [
        (0, "3fec800000000000"), # drsqrt
        (1, "3fec0e4466666667"), # 1Newton
        (2, "3fec10db9ec87526"), # 2Newton
        (3, "3fec10dbfab3c6c0"), # 3Newton
        (4, "3fec10dbfab3c885"), # 4Newton
        (5, "3fec10dbfab3c884"), # 5Newton
    ]

    # 単精度データ (Single)
    data_points_single = [
        (0, "0x3f640000"),
        (1, "0x3f607224"),
        (2, "0x3f6086de"),
        (3, "0x3f6086e0"),
        (4, "0x3f6086e0"),
        (5, "0x3f6086e0"),
    ]

    # --- 計算処理 ---
    iters_d, errors_d = [], []
    iters_s, errors_s = [], []
    
    # マシンイプシロン（グラフの0対策）
    # 倍精度用: 1e-16, 単精度用は便宜上 1e-9 程度にしておく
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
        # 単精度の限界値付近でこれ以上下がらない場合、値は残る
        if error == 0.0: error = eps_single
        iters_s.append(i)
        errors_s.append(error)

    # --- グラフ描画設定 ---
    plt.rcParams.update({'font.size': 20})
    plt.figure(figsize=(10, 6))
    
    # Double Precision (Navy, Circle)
    plt.plot(iters_d, errors_d, marker='o', linestyle='-', color='navy', 
             label='Double Precision', markersize=10, linewidth=2.5)

    # Single Precision (Orange/Red, Square) - 比較用に追加
    plt.plot(iters_s, errors_s, marker='s', linestyle='--', color='tab:red', 
             label='Single Precision', markersize=10, linewidth=2.5)
    
    plt.yscale('log')
    plt.xlabel('Number of Iterations', fontsize=18)
    plt.ylabel('Absolute Error', fontsize=18)
    
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.xticks(iters_d)
    plt.legend(fontsize=16) # 凡例を表示
    
    plt.tight_layout()
    
    # --- 保存処理 ---
    save_dir = r'/home/kazuki/thesis/images' 
    filename = 'newton_r=1.3.pdf' 
    
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)

    plt.savefig(save_path, dpi=300)
    print(f"Graph saved as {save_path}")

    # plt.show()

if __name__ == "__main__":
    main()