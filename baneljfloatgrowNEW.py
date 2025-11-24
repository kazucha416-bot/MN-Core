import os

def main():
    # --- 設定 ---
    filepath = "/home/kazuki/mncore/baneljfloat.vsm"
    loop_count = 2000   # 2000ステップ
    skip_step = 10      # 10ステップに1回保存
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    print(f"単精度アセンブリコード(間引き保存版)を {filepath} に書き出します...")

    # 保存回数カウンタ
    save_count = 0

    with open(filepath, "w") as f:
        # --- 1. 初期化ブロック (共通) ---
        f.write("""d set $lm0n0c0b0m0p0 5 3fa666663fa666663a83126f3a83126f3f8000003f8000003f8000003f8000003f8000003f800000
d set $ln0n0c0b0m0p0 1 0000000000000000

imm f"4.0" $t
fvmul $lm8 $lm8 $nowrite
fvmul $mauf $lm8 $nowrite
fvmul $mauf $mauf $lr0
fvmul $t $lm6 $ls0
nop
fvmul $lr0 $lr0 $lr2
fvmul $ls0 $lr0 $lr0
nop/2
fvmul $ls0 $lr2 $lr2
imm f"6.0" $nowrite
fvmul $aluf $lr0 $ls0
imm f"12.0" $nowrite
fvmul $aluf $lr2 $ls2

#最初の力を計算
fvmul $lm0 $lm0 $lr4
nop/2
frsqrt $lr4 $nowrite
fvmul $aluf $aluf $ls4
nop
imm f"2.0" $nowrite
fvfma $lr4 -$ls4 $aluf $nowrite
nop/2
fvmul $ls4 $mauf $lr6 #r2iが求まった
nop/2
fvmul $lr6 $lr6 $ls6
nop/2
fvmul $lr6 $ls6 $lr8 #r06iが求まった
nop/2
fvmul $lr8 $lr8 $lr10 #r12iが求まった
nop
fvmul $ls0 $lr8 $nowrite
fvfma $ls2 $lr10 -$mauf $nowrite
fvmul $mauf $lr6 $ls8 #fcが求まった
nop/2
fvmul $ls8 $lm0 $ls10 #f1が求まった

#1/massの配列を作る
frsqrt $lm4 $nowrite
fvmul $aluf $aluf $ls4
nop
imm f"2.0" $nowrite
fvfma $lm4 -$ls4 $aluf $nowrite
nop/2
fvmul $ls4 $mauf $lm10  #1/massが求まった
nop/2
fvmul $lm10 $ls10 $ls12  #f1/mass

#dt*dt*0.5を作る
fvmul $lm2 $lm2 $ln2
imm f"0.5" $nowrite
nop
fvmul $ln2 $aluf $lr12 #0.5*h*hが求まった

# pos + h*v の計算
fvpassa $lm2 $lr14

""")

        # --- 2. ループ部分 ---
        for k in range(loop_count):
            f.write(f"""# Loop {k}
fvpassa $ln0 $ls14
nop/2
fvfma $lr14 $ls14 $lm0 $nowrite
fvfma $lr12 $ls12 $mauf $lm0
nop/2
fvmul $lm0 $lm0 $lr4
nop/2
frsqrt $lr4 $nowrite
fvmul $aluf $aluf $ls4
nop
imm f"2.0" $nowrite
fvfma $lr4 -$ls4 $aluf $nowrite
nop/2
fvmul $ls4 $mauf $lr6
nop/2
fvmul $lr6 $lr6 $ls6
nop/2
fvmul $lr6 $ls6 $lr8
nop/2
fvmul $lr8 $lr8 $lr10
nop
fvmul $ls0 $lr8 $nowrite
fvfma $ls2 $lr10 -$mauf $nowrite
fvmul $mauf $lr6 $ls16
nop/2
fvmul $ls16 $lm0 $lr16
imm f"0.5" $nowrite
fvmul $aluf $lm2 $t
fvadd $ls10 $lr16 $nowrite
fvfma $mauf $t $ln0 $ln0
fvpassa $lr16 $ls10
fvpassa $lr8 $nowrite
fvmul $mauf $lr0 $t
fvpassa $lr10 $nowrite
fvfma $lr2 $mauf -$t $lm12
imm f"0.5" $nowrite
nop
fvmul $aluf $lm4 $t
nop/2
fvmul $ln0 $ln0 $nowrite
nop/2
fvmul $mauf $t $lm14
nop/2
fvpassa $lm14 $nowrite
fvadd $mauf $lm12 $nowrite
fvpassa $mauf $lm16

""")
            # --- 間引き保存ブロック ---
            if k % skip_step == 0:
                # アドレス計算 (保存1回につき16進める)
                base_addr = save_count * 16
                
                f.write(f"""
nop/2
l1bmm@0 $lm16 $lb{base_addr}      # TotalE
l1bmm@0 $lm0 $lb{base_addr + 4}   # Pos
l1bmm@0 $lm12 $lb{base_addr + 8}  # PE
l1bmm@0 $lm14 $lb{base_addr + 12} # KE

""")
                save_count += 1

        # --- 3. 終了ブロック ---
        # 最後のデータサイズは 保存回数 * 16
        total_data_size = save_count * 16

        f.write(f"""
d getf $lm0n0c0b0m0p0 16
d getf $ln0n0c0b0m0p0 16
d getf $lr0n0c0b0m0p0 16
d getf $ls0n0c0b0m0p0 16
d getf $lb0n0c0b0 {total_data_size}
""")

    print(f"完了しました。(保存回数: {save_count}回, L1BM使用量: {total_data_size}語)")

if __name__ == "__main__":
    main()
