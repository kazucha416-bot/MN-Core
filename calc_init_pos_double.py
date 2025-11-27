import struct

def to_hex(val):
    """倍精度浮動小数点数(64bit)を16桁の16進数文字列に変換"""
    return struct.pack('>d', val).hex()

def main():
    # --- Cコードのパラメータ ---
    a = 2.0
    nx, ny, nz = 1, 1, 1
    num = 4
    
    # pos[3][num] の初期化
    pos = [[0.0] * num for _ in range(3)]
    
    # pos0 の定義 (Cコードと同じ)
    # pos0[0]: x, pos0[1]: y, pos0[2]: z
    pos0 = [
        [0.0, 0.0, a/2.0, a/2.0],
        [0.0, a/2.0, a/2.0, 0.0],
        [0.0, a/2.0, 0.0, a/2.0]
    ]
    
    # --- 位置の計算 ---
    n = -1
    # range(1, nx + 1) は 1 から nx まで
    for jx in range(1, nx + 1):
        for jy in range(1, ny + 1):
            for jz in range(1, nz + 1):
                # 単位格子内の4粒子を配置
                for k in range(4):
                    n += 1
                    if n >= num: break
                    
                    # (jx - 1) * a はオフセット
                    offset_x = (jx - 1) * a
                    offset_y = (jy - 1) * a
                    offset_z = (jz - 1) * a
                    
                    pos[0][n] = pos0[0][k] + offset_x
                    pos[1][n] = pos0[1][k] + offset_y
                    pos[2][n] = pos0[2][k] + offset_z

    # --- 結果出力 ---
    print(f"--- Position (a={a}, nx={nx}, ny={ny}, nz={nz}) ---")
    
    dims = ["x", "y", "z"]
    
    # 各次元ごとに表示
    for i in range(3):
        row_str = ""
        print(f"pos_{dims[i]}:")
        for j in range(num):
            val = pos[i][j]
            hex_val = to_hex(val)
            print(f"  Particle {j}: {hex_val}  ({val})")
            row_str += hex_val
        
        print(f"  -> Linear string for 'd set': {row_str}")
        print("")

if __name__ == "__main__":
    main()
