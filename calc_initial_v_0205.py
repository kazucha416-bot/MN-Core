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
    # --- 設定エリア ---
    num = 4
    speed_min = 0.5  # 速さの最小値
    speed_max = 1.0  # 速さの最大値
    random.seed(42)  # シード固定
    # ------------------

    # --- 1. 初期化 (ランダムな方向 + 指定範囲の速さ) ---
    v = [[0.0] * num for _ in range(3)]
    
    for j in range(num):
        # -1.0 ~ 1.0 のランダムな方向ベクトルを作成
        vx = random.uniform(-1.0, 1.0)
        vy = random.uniform(-1.0, 1.0)
        vz = random.uniform(-1.0, 1.0)
        
        # 正規化（長さ1のベクトルにする）
        norm = math.sqrt(vx*vx + vy*vy + vz*vz)
        if norm == 0: norm = 1.0
        
        # 指定範囲(0.5 ~ 1.0)からランダムな速さを選んで掛ける
        target_speed = random.uniform(speed_min, speed_max)
        
        v[0][j] = (vx / norm) * target_speed
        v[1][j] = (vy / norm) * target_speed
        v[2][j] = (vz / norm) * target_speed

    # --- 2. 重心速度のキャンセル (必須) ---
    # これをやらないと系全体がドリフトします。
    # ※これをやると、設定した速さ(0.5~1.0)からわずかに値がズレますが、MDとして正しい挙動です。
    vmean = [0.0] * 3
    for i in range(3):
        vmean[i] = sum(v[i]) / num

    for j in range(num):
        v[0][j] -= vmean[0]
        v[1][j] -= vmean[1]
        v[2][j] -= vmean[2]

    # --- 3. 結果確認用の表示 (ご要望箇所) ---
    print("=" * 60)
    print("【初期速度の確認 (Decimal)】")
    print(f"Target Speed Range: {speed_min} ~ {speed_max}")
    print("-" * 60)
    print(f"{'Particle':^8} | {'vx':^10} {'vy':^10} {'vz':^10} | {'Speed (|v|)':^12}")
    print("-" * 60)
    
    for j in range(num):
        vx = v[0][j]
        vy = v[1][j]
        vz = v[2][j]
        speed = math.sqrt(vx**2 + vy**2 + vz**2)
        print(f"   {j:^5} | {vx:9.5f}  {vy:9.5f}  {vz:9.5f} | {speed:9.5f}")
    
    print("=" * 60)
    print("\n")


    # --- 4. 16進数データの出力 (MN-Core用) ---
    
    # (B) 次元ごとの羅列
    # print("--- v (Dimension-major) ---") 
    # (省略: 以前のコードが必要ならコメントアウトを外してください)

    # (C) [メイン] 粒子ごとの羅列 (4列形式・パディング対応)
    print("-" * 60)
    print("--- 4 Columns Format (Padded for MN-Core Memory Layout) ---")
    print("Format: [Val 00..] [Val 00..] [Val 00..] [00..00..]")
    print("-" * 60)
    
    row_double_bundled = []
    row_float_padded_bundled = []

    for j in range(num):
        # --- Double ---
        d_chunk = to_double_hex(v[0][j]) + to_double_hex(v[1][j]) + to_double_hex(v[2][j])
        row_double_bundled.append(d_chunk)

        # --- Float (Padding) ---
        vx_str = to_float_hex(v[0][j]) + "00000000"
        vy_str = to_float_hex(v[1][j]) + "00000000"
        vz_str = to_float_hex(v[2][j]) + "00000000"
        padding_end = "0000000000000000"
        
        f_chunk = vx_str + vy_str + vz_str + padding_end
        row_float_padded_bundled.append(f_chunk)

    print("[Double (64bit)]")
    print("  ".join(row_double_bundled))
    
    print("\n[Float (32bit, Padded to 64bit stride + End Padding)]")
    print("  ".join(row_float_padded_bundled))

if __name__ == "__main__":
    main()