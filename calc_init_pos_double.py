import struct

def to_double_hex(val):
    return struct.pack('>d', val).hex()

def to_float_hex(val):
    return struct.pack('>f', val).hex()

def main():
    # --- パラメータ ---
    a = 2.0
    num = 4
    
    # pos[3][num] 初期化
    pos = [[0.0] * num for _ in range(3)]
    
    # 基本配置
    pos0 = [
        [0.0, 0.0, a/2.0, a/2.0], # x
        [0.0, a/2.0, a/2.0, 0.0], # y
        [0.0, a/2.0, 0.0, a/2.0]  # z
    ]
    
    # --- 位置計算 (格子生成) ---
    n = -1
    for jx in range(1, 2):
        for jy in range(1, 2):
            for jz in range(1, 2):
                for k in range(4):
                    n += 1
                    if n >= num: break
                    offset_x, offset_y, offset_z = (jx-1)*a, (jy-1)*a, (jz-1)*a
                    pos[0][n] = pos0[0][k] + offset_x
                    pos[1][n] = pos0[1][k] + offset_y
                    pos[2][n] = pos0[2][k] + offset_z

    # --- 出力処理 ---
    print(f"--- 4 Columns Format (Padded for MN-Core Memory Layout) ---\n")
    print("Format: [Val 00..] [Val 00..] [Val 00..] [00..00..] (Total 256bit)\n")

    # データ格納用リスト
    row_double = []
    row_float = []

    for j in range(num):
        # 粒子jの x, y, z を取得
        
        # --- Double (そのまま) ---
        # 64bit * 3 = 192bit (余り部分は詰めないのが通常のDouble配置ですが、必要ならここも0埋めできます)
        # 今回は前のコードに合わせて x,y,z の連結のみにします
        d_chunk = to_double_hex(pos[0][j]) + to_double_hex(pos[1][j]) + to_double_hex(pos[2][j])
        row_double.append(d_chunk)

        # --- Float (パディング処理) ---
        # 1. 各成分(32bit)の後ろに 00000000 (32bit zero) を付与 -> 64bit幅確保
        x_str = to_float_hex(pos[0][j]) + "00000000"
        y_str = to_float_hex(pos[1][j]) + "00000000"
        z_str = to_float_hex(pos[2][j]) + "00000000"
        
        # 2. 最後に 0000000000000000 (64bit zero) を付与 -> 全体で256bit(4長語)にする
        padding_end = "0000000000000000"
        
        f_chunk = x_str + y_str + z_str + padding_end
        row_float.append(f_chunk)

    # 横並び表示
    print("[Double (64bit)]")
    print("  ".join(row_double))
    
    print("\n[Float (32bit, Padded to 64bit stride + End Padding)]")
    print("  ".join(row_float))

if __name__ == "__main__":
    main()