import os

def main():
    # 設定
    filepath = "/home/kazuki/mncore/banemasunew.vsm"
    loop_count = 70
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    print(f"ばね問題をEuler法を用いて解析するvsm（発散していくバージョン）を {filepath} に書き出します...(20251204作成)")

    with open(filepath, "w") as f:
        # --- 1. 初期化ブロック ---
        f.write("""
# lm0v h=0.1 lm8v h*k/m=0.1 lm16v 0.5(Eの計算用)
d set $lm0n0c0b0m0p0 12 3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3dcccccd3f0000003f0000003f0000003f0000003f0000003f0000003f0000003f000000
# $lr0v v0=0
d set $lr0n0c0b0m0p0 1 0000000000000000
# $ls0v x0=1.0
d set $ls0n0c0b0m0p0 1 3f8000003f800000
""")

        # --- 2. ループ部分 ---
        for k in range(loop_count):
            lb_addr = k * 4
            
            f.write(f"""
fvfma $lm0v $lr0v $ls0v $ln0v # x(i+1)=x(i)+h*v(i)
fvfma -$lm8v $ls0v $lr0v $lr0v # v(i+1)=v(i)-h*k/m*x(i)
nop
fvpassa $ln0v $ls0v
fvmul $lr0v $lr0v $lr64v
fvmul $ls0v $ls0v $nowrite
fvadd $lr64v $mauf $nowrite
fvmul $lm16v $mauf $nowrite
l1bmm@0 $mauf $lb{lb_addr}
""")

        # --- 3. 終了ブロック ---
        f.write(f"""
d getf $lm0n0c0b0m0p0 12
d getf $ln0n0c0b0m0p0 4
d getf $lr0n0c0b0m0p0 4
d getf $ls0n0c0b0m0p0 4
d getf $lb0n0c0b0 {4 * loop_count}
""")

    print("完了しました。")

if __name__ == "__main__":
    main()
