import random
import math
import struct

def to_hex(val):
    """倍精度浮動小数点数(64bit)を16桁の16進数文字列に変換"""
    # >d : Big-endian double
    return struct.pack('>d', val).hex()

def main():
    num = 4
    temp0 = 1.0
    
    # 乱数シード固定 (再現性のため)
    # Cコードの srand(time(NULL)) とは異なりますが、実行のたびに同じ結果が出ます
    random.seed(42)
    
    # --- 1. 初期化 (Random) ---
    v = [[0.0] * num for _ in range(3)]
    vmean = [0.0] * 3
    
    for i in range(3):
        sum_v = 0.0
        for j in range(num):
            # -1.0 ～ 1.0 の乱数
            val = random.random() * 2.0 - 1.0
            v[i][j] = val
            sum_v += val
        vmean[i] = sum_v / num

    # --- 2. 重心速度のキャンセル ---
    for j in range(num):
        v[0][j] = v[0][j] - vmean[0]
        v[1][j] = v[1][j] - vmean[1]
        v[2][j] = v[2][j] - vmean[2]
        
    # --- 3. 温度スケーリング ---
    ke = 0.0
    for j in range(num):
        # 0.5 * v^2 (mass=1.0)
        v2 = v[0][j]**2 + v[1][j]**2 + v[2][j]**2
        ke += 0.5 * v2
        
    ke /= num
    temp = ke / 1.5
    scale_factor = math.sqrt(temp0 / temp)
    
    for i in range(3):
        for j in range(num):
            v[i][j] *= scale_factor

    # --- 4. 結果出力 (16桁16進数) ---
    print("--- vmean (3 elements) ---")
    print(f"vx_mean: {to_hex(vmean[0])}  ({vmean[0]})")
    print(f"vy_mean: {to_hex(vmean[1])}  ({vmean[1]})")
    print(f"vz_mean: {to_hex(vmean[2])}  ({vmean[2]})")
    print("")

    print("--- v (3x4 matrix) ---")
    dims = ["x", "y", "z"]
    for i in range(3):
        row_str = ""
        print(f"v{dims[i]}:")
        for j in range(num):
            hex_val = to_hex(v[i][j])
            print(f"  Particle {j}: {hex_val}  ({v[i][j]})")
            row_str += hex_val
        print(f"  -> Linear string for 'd set': {row_str}")

if __name__ == "__main__":
    main()
