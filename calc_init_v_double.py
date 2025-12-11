import random
import math
import struct

def to_double_hex(val):
    """倍精度浮動小数点数(64bit)を16桁の16進数文字列に変換"""
    return struct.pack('>d', val).hex()

def to_float_hex(val):
    """単精度浮動小数点数(32bit)を8桁の16進数文字列に変換"""
    return struct.pack('>f', val).hex()

def main():
    num = 4
    temp0 = 1.0
    
    # 乱数シード固定
    random.seed(42)
    
    # --- 1. 初期化 (Random) ---
    v = [[0.0] * num for _ in range(3)]
    vmean = [0.0] * 3
    
    for i in range(3):
        sum_v = 0.0
        for j in range(num):
            val = random.random() * 2.0 - 1.0
            v[i][j] = val
            sum_v += val
        vmean[i] = sum_v / num

    # --- 2. 重心速度のキャンセル ---
    for j in range(num):
        v[0][j] -= vmean[0]
        v[1][j] -= vmean[1]
        v[2][j] -= vmean[2]
        
    # --- 3. 温度スケーリング ---
    ke = 0.0
    for j in range(num):
        v2 = v[0][j]**2 + v[1][j]**2 + v[2][j]**2
        ke += 0.5 * v2
        
    ke /= num
    temp = ke / 1.5
    scale_factor = math.sqrt(temp0 / temp)
    
    for i in range(3):
        for j in range(num):
            v[i][j] *= scale_factor
            
    # --- 4. 結果出力 ---
    
    # (A) 平均速度 (デバッグ用)
    print("--- vmean (3 elements) ---")
    dims = ["x", "y", "z"]
    for i in range(3):
        print(f"v{dims[i]}_mean: {vmean[i]}")
    print("")

    # (B) 次元ごとの羅列 (Linear String)
    # ここも一応パディングルールを適用しておきますが、メインは(C)です
    print("--- v (Dimension-major) ---")
    for i in range(3):
        row_str_f_padded = ""
        for j in range(num):
            h_f = to_float_hex(v[i][j])
            # 値(8桁) + パディング(8桁)
            row_str_f_padded += h_f + "00000000"
        
        # 最後に16桁(4長語アライメント調整)は次元単位だと意味が薄いかもしれませんが
        # 要望があればここにも追加できます。今回は(C)をメインにします。
        print(f"v{dims[i]} (Float Padded): {row_str_f_padded}")
    print("")

    # (C) [メイン] 粒子ごとの羅列 (4列形式・パディング対応)
    print("-" * 60)
    print("--- 4 Columns Format (Padded for MN-Core Memory Layout) ---")
    print("Format: [Val 00..] [Val 00..] [Val 00..] [00..00..]")
    print("-" * 60)
    
    row_double_bundled = []
    row_float_padded_bundled = []

    for j in range(num):
        # --- Double (そのまま) ---
        d_chunk = to_double_hex(v[0][j]) + to_double_hex(v[1][j]) + to_double_hex(v[2][j])
        row_double_bundled.append(d_chunk)

        # --- Float (パディング処理) ---
        # 1. 各成分の後ろに 00000000 (32bit zero) を付与 -> これで64bit幅になる
        vx_str = to_float_hex(v[0][j]) + "00000000"
        vy_str = to_float_hex(v[1][j]) + "00000000"
        vz_str = to_float_hex(v[2][j]) + "00000000"
        
        # 2. 最後に 0000000000000000 (64bit zero) を付与 -> これで全体が4長語(256bit)になる
        padding_end = "0000000000000000"
        
        f_chunk = vx_str + vy_str + vz_str + padding_end
        row_float_padded_bundled.append(f_chunk)

    print("[Double (64bit)]")
    print("  ".join(row_double_bundled))
    
    print("\n[Float (32bit, Padded to 64bit stride + End Padding)]")
    print("  ".join(row_float_padded_bundled))

if __name__ == "__main__":
    main()