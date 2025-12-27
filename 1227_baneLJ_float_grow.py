def generate_vsm_float(filename, total_steps=2000):
    # --- 1. 初期化ブロック (単精度化済み) ---
    # ルール: Float32のHex(8桁) + "00000000"
    
    # 変換メモ:
    # 1.3   (3ff4...) -> 3fa66666
    # 0.001 (3f50...) -> 3a83126f
    # 1.0   (3ff0...) -> 3f800000
    # 1e-6  (3eb0...) -> 358637bd
    # 0.0   (0000...) -> 00000000
    # 0.5   (3fe0...) -> 3f000000
    # 4.0   (4010...) -> 40800000
    # 24.0  (4038...) -> 41c00000
    # 48.0  (4048...) -> 42400000
    # 1.5   (3ff8...) -> 3fc00000

    init_code = [
        # $lm0: x=1.3, h=0.001, m=1.0, eps=1.0, sig=1.0, 1/m=1.0, h^2=1e-6
        "d set $lm0n0c0b0m0p0 7 3fa66666000000003a83126f000000003f800000000000003f800000000000003f800000000000003f80000000000000358637bd00000000",
        
        # $ln0: v0=0.0, h^2=1e-6, 0.5
        "d set $ln0n0c0b0m0p0 3 0000000000000000358637bd000000003f00000000000000",
        
        # $lr0: ce06=4.0, ce12=4.0
        "d set $lr0n0c0b0m0p0 2 40800000000000004080000000000000",
        
        # $ls0: cf06=24.0, cf12=48.0, 1.5
        "d set $ls0n0c0b0m0p0 3 41c000000000000042400000000000003fc0000000000000",

        # --- 以下、単精度命令 (d->f, u除去) ---
        "frsqrt $lm0 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $nowrite",
        "fvmul $mauf $mauf $lr8",
        "nop/2",
        "fvmul $lr8 $lr8 $nowrite",
        "fvmul $mauf $lr8 $lr10",
        "nop/2",
        "fvmul $lr10 $lr10 $lr12",
        "nop",
        "fvmul $ls0 $lr10 $nowrite",
        "fvfma $ls2 $lr12 -$mauf $nowrite",
        "fvmul $mauf $lr8 $ls8",
        "nop/2",
        "fvmul $ls8 $lm0 $ls10",
        "fvmul $ln4 $lm12 $lr14",
        "nop"
    ]

    # --- 2. 時間発展ループブロック ---
    physics_code = [
        "fvmul $ls10 $lm10 $ls12",
        "nop/2",
        "fvfma $lr14 $ls12 $lm0 $nowrite",
        "fvfma $lm2 $ln0 $mauf $nowrite",
        "fvpassa $mauf $lm0",
        "nop/2",
        "frsqrt $lm0 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $ls6",
        "nop/2",
        "fvmul $lm0 $ls6 $lr6",
        "nop/2",
        "fvfma $lr6 -$ln4 $ls4 $nowrite",
        "fvmul $mauf $lr4 $lr4",
        "nop/2",
        "fvmul $lr4 $lr4 $nowrite",
        "fvmul $mauf $mauf $lr8",
        "nop/2",
        "fvmul $lr8 $lr8 $nowrite",
        "fvmul $mauf $lr8 $lr10",
        "nop/2",
        "fvmul $lr10 $lr10 $lr12",
        "nop",
        "fvmul $ls0 $lr10 $nowrite",
        "fvfma $ls2 $lr12 -$mauf $nowrite",
        "fvmul $mauf $lr8 $ls8",
        "nop/2",
        "fvmul $ls8 $lm0 $lr16",
        "fvmul $ln4 $lm2 $lr18",
        "nop",
        "fvadd $ls10 $lr16 $nowrite",
        "fvmul $mauf $lm10 $nowrite",
        "fvfma $mauf $lr18 $ln0 $ln0",
        "fvpassa $lr16 $ls10",
        "nop/2"
    ]

    # --- 3. エネルギー出力ブロック ---
    energy_code_template = [
        "fvpassa $lr2 $nowrite",
        "fvmul $mauf $lr12 $ls20",
        "nop",
        "fvpassa $lr10 $nowrite",
        "fvfma $mauf -$lr0 $ls20 $lm14",
        "nop/2",
        "fvmul $ln4 $lm4 $lr22",
        "nop",
        "fvmul $ln0 $ln0 $nowrite",
        "fvmul $mauf $lr22 $lm16",
        "nop/2",
        "fvpassa $lm16 $nowrite",
        "fvadd $mauf $lm14 $nowrite",
        "l1bmm@0 $mauf $lb{}"
    ]

    # --- 4. 最終出力ブロック ---
    final_output_code = [
        "d getf $lm0n0c0b0m0p0 10",
        "d getf $ln0n0c0b0m0p0 4",
        "d getf $lr0n0c0b0m0p0 12",
        "d getf $ls0n0c0b0m0p0 8",
        "d getf $lb0n0c0b0 8000"
    ]

    # === 書き込み処理 ===
    with open(filename, 'w') as f:
        # 1. 初期化
        for line in init_code:
            f.write(line + "\n")
        
        lb_offset = 0

        # 2. ループ展開
        print(f"Generating {total_steps} steps (Float version)...")
        for step in range(1, total_steps + 1):
            # 物理計算
            for line in physics_code:
                f.write(line + "\n")
            
            # 出力 (Step 1 or 10の倍数)
            if step == 1 or step % 10 == 0:
                for line in energy_code_template:
                    if "l1bmm" in line:
                        f.write(line.format(lb_offset) + "\n")
                    else:
                        f.write(line + "\n")
                lb_offset += 16

        # 3. 最終出力
        for line in final_output_code:
            f.write(line + "\n")

    print(f"Done! Float VSM generated: {filename}")

if __name__ == "__main__":
    generate_vsm_float("1227_float_baneLJ.vsm", total_steps=2000)