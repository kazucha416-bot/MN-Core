import struct
import matplotlib.pyplot as plt
import os  

def hex_to_double(hex_str):
    """16進数文字列(64bit)を倍精度浮動小数点数に変換"""
    int_val = int(hex_str, 16)
    return struct.unpack('>d', struct.pack('>Q', int_val))[0]

def main():
    # --- データ定義 ---
    actual_val = 1 / (3.0 ** 0.5)  # 3.0の平方根の逆数の実際の値
    
    data_points = [
        (0, "3fe2000000000000"), # drsqrt
        (1, "3fe2750000000000"), # 1Newton
        (2, "3fe279a583a32000"), # 2Newton
        (3, "3fe279a7458ff2e9"), # 3Newton
        (4, "3fe279a74590331c"), # 4Newton
        (5, "3fe279a74590331c"), # 5Newton
    ]

    # --- 計算処理 (修正版) ---
    iterations = []
    errors = []
    
    # マシンイプシロン（倍精度の限界）に近い値
    machine_epsilon = 1e-16

    for i, hex_str in data_points:
        val = hex_to_double(hex_str)
        error = abs(val - actual_val)
        
        # 誤差が0になったら、グラフ表示用に最小値を代入する
        if error == 0.0:
            error = machine_epsilon # 便宜上 1e-16 としてプロット
            print(f"Iter {i}: Converged to exact match! (Error=0)") # 確認用ログ
        
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
    plt.xlabel('Number of Iterations', fontsize=18)
    plt.ylabel('Absolute Error', fontsize=18)
    
    plt.grid(True, which="both", ls="--", alpha=0.7)
    plt.xticks(iterations)
    
    # レイアウト調整
    plt.tight_layout()
    
    # --- 保存処理 ---
    # 保存先のディレクトリとファイル名
    save_dir = r'/home/kazuki/mncore' 
    filename = 'newton_error_plot_r=3.0.pdf'  # 画質最強のPDFに変更しておきました！（PNGが良ければ.pngに戻してね）
    
    # パスを結合
    save_path = os.path.join(save_dir, filename)

    # ディレクトリが存在しない場合に備えて、なければ作る（念のため）
    os.makedirs(save_dir, exist_ok=True)

    # 保存実行
    plt.savefig(save_path, dpi=300)
    print(f"Graph saved as {save_path}")

    # plt.show() # 確認したいときはここを外す

if __name__ == "__main__":
    main()