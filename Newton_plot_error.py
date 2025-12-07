import struct
import matplotlib.pyplot as plt

def hex_to_double(hex_str):
    """16進数文字列(64bit)を倍精度浮動小数点数に変換"""
    int_val = int(hex_str, 16)
    return struct.unpack('>d', struct.pack('>Q', int_val))[0]

def main():
    # --- データ定義 ---
    actual_val = 0.8770580193
    
    data_points = [
        (0, "3fec800000000000"), # drsqrt
        (1, "3fec0e4466666667"), # 1Newton
        (2, "3fec10db9ec87526"), # 2Newton
        (3, "3fec10dbfab3c6c0"), # 3Newton
        (4, "3fec10dbfab3c885"), # 4Newton
        (5, "3fec10dbfab3c884"), # 5Newton
    ]

    # --- 計算処理 ---
    iterations = []
    errors = []
    
    for i, hex_str in data_points:
        val = hex_to_double(hex_str)
        error = abs(val - actual_val)
        iterations.append(i)
        errors.append(error)

    # --- グラフ描画設定 ---
    # 文字サイズを全体的に大きく設定
    plt.rcParams.update({'font.size': 20})

    plt.figure(figsize=(10, 6))
    
    # 線の色をネイビーに、線幅やマーカーも少し強調
    plt.plot(iterations, errors, marker='o', linestyle='-', color='navy', 
             label='Absolute Error', markersize=10, linewidth=2.5)
    
    plt.yscale('log')
    plt.title(r'Error Reduction of Newton Method ($1.3^{-0.5}$)', fontsize=22)
    plt.xlabel('Number of Iterations', fontsize=18)
    plt.ylabel('Absolute Error', fontsize=18)
    
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.xticks(iterations)
    
    # レイアウト調整
    plt.tight_layout()
    
    # 保存
    filename = 'newton_error_plot_navy.png'
    plt.savefig(filename, dpi=300)
    print(f"Graph saved as {filename}")
    
    # plt.show() # 必要に応じてコメントアウトを外してください

if __name__ == "__main__":
    main()