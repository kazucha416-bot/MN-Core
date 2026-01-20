import struct

def generate_initial_values():
    # --- 設定 ---
    start_r = 0.5
    step = 0.04
    num_points = 61  # 0.5 から 2.9 まで
    
    # 結果を格納する文字列
    output_string = ""
    
    # --- ループ計算 ---
    for i in range(num_points):
        # r の値を計算
        r = start_r + (i * step)
        
        # double(64bit) を ビッグエンディアンのバイト列に変換し、16進数文字列化
        # '>d' は Big-endian double precision float を意味します
        # 単精度の '>f' と違い、これだけで64bit（16桁）の文字列になります
        double_hex = struct.pack('>d', r).hex()
        
        # 以前のようなゼロ埋め（+ "00000000"）は不要なので、そのまま連結
        output_string += double_hex

    # --- コンソール出力 ---
    print(output_string)

if __name__ == "__main__":
    generate_initial_values()