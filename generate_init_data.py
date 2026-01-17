import struct

def generate_initial_values():
    # --- 設定 ---
    start_r = 0.5
    step = 0.04
    num_points = 61  # 0.5 から 2.9 まで 0.04 刻みだとちょうど61点 (0.5 + 0.04*60 = 2.9)
    
    # 結果を格納する文字列
    output_string = ""
    
    # --- ループ計算 ---
    for i in range(num_points):
        # r の値を計算
        r = start_r + (i * step)
        
        # float(32bit) を ビッグエンディアンのバイト列に変換し、16進数文字列化
        # '>f' は Big-endian single precision float を意味します
        float_hex = struct.pack('>f', r).hex()
        
        # 後ろをゼロ8個で埋める
        padded_hex = float_hex + "00000000"
        
        # 隙間なく連結
        output_string += padded_hex

    # --- コンソール出力 ---
    print(output_string)

if __name__ == "__main__":
    generate_initial_values()