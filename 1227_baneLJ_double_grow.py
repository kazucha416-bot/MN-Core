def generate_vsm_final(filename, total_steps=2000):
    # --- 1. 初期化ブロック ---
    init_code = [
        "d set $lm0n0c0b0m0p0 7 3ff4cccccccccccd3f50624dd2f1a9fc3ff00000000000003ff00000000000003ff00000000000003ff00000000000003eb0c6f7a0b5ed8d",
        "d set $ln0n0c0b0m0p0 3 00000000000000003eb0c6f7a0b5ed8d3fe0000000000000",
        "d set $lr0n0c0b0m0p0 2 40100000000000004010000000000000",
        "d set $ls0n0c0b0m0p0 3 403800000000000040480000000000003ff8000000000000",
        "drsqrt $lm0 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $nowrite",
        "dvmulu $mauf $mauf $lr8",
        "nop/2",
        "dvmulu $lr8 $lr8 $nowrite",
        "dvmulu $mauf $lr8 $lr10",
        "nop/2",
        "dvmulu $lr10 $lr10 $lr12",
        "nop",
        "dvmulu $ls0 $lr10 $nowrite",
        "dvfmau $ls2 $lr12 -$mauf $nowrite",
        "dvmulu $mauf $lr8 $ls8",
        "nop/2",
        "dvmulu $ls8 $lm0 $ls10",
        "dvmulu $ln4 $lm12 $lr14",
        "nop"
    ]

    # --- 2. 時間発展ループブロック (最後にnop/2を追加) ---
    physics_code = [
        "dvmulu $ls10 $lm10 $ls12",
        "nop/2",
        "dvfmau $lr14 $ls12 $lm0 $nowrite",
        "dvfmau $lm2 $ln0 $mauf $nowrite",
        "dvpassa $mauf $lm0",
        "nop/2",
        "drsqrt $lm0 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $ls6",
        "nop/2",
        "dvmulu $lm0 $ls6 $lr6",
        "nop/2",
        "dvfmau $lr6 -$ln4 $ls4 $nowrite",
        "dvmulu $mauf $lr4 $lr4",
        "nop/2",
        "dvmulu $lr4 $lr4 $nowrite",
        "dvmulu $mauf $mauf $lr8",
        "nop/2",
        "dvmulu $lr8 $lr8 $nowrite",
        "dvmulu $mauf $lr8 $lr10",
        "nop/2",
        "dvmulu $lr10 $lr10 $lr12",
        "nop",
        "dvmulu $ls0 $lr10 $nowrite",
        "dvfmau $ls2 $lr12 -$mauf $nowrite",
        "dvmulu $mauf $lr8 $ls8",
        "nop/2",
        "dvmulu $ls8 $lm0 $lr16",
        "dvmulu $ln4 $lm2 $lr18",
        "nop",
        "dvadd $ls10 $lr16 $nowrite",
        "dvmulu $mauf $lm10 $nowrite",
        "dvfmau $mauf $lr18 $ln0 $ln0",
        "dvpassa $lr16 $ls10",
        "nop/2" # ★追加: ループの区切り用
    ]

    # --- 3. エネルギー出力ブロック ---
    energy_code_template = [
        "dvpassa $lr2 $nowrite",
        "dvmulu $mauf $lr12 $ls20",
        "nop",
        "dvpassa $lr10 $nowrite",
        "dvfmau $mauf -$lr0 $ls20 $lm14",
        "nop/2",
        "dvmulu $ln4 $lm4 $lr22",
        "nop",
        "dvmulu $ln0 $ln0 $nowrite",
        "dvmulu $mauf $lr22 $lm16",
        "nop/2",
        "dvpassa $lm16 $nowrite",
        "dvadd $mauf $lm14 $nowrite",
        "l1bmm@0 $mauf $lb{}"  # アドレスが入る
    ]

    # --- 4. 最終出力ブロック ---
    final_output_code = [
        "d getd $lm0n0c0b0m0p0 10",
        "d getd $ln0n0c0b0m0p0 4",
        "d getd $lr0n0c0b0m0p0 12",
        "d getd $ls0n0c0b0m0p0 8",
        "d getd $lb0n0c0b0 8000"
    ]

    # === 書き込み処理 ===
    with open(filename, 'w') as f:
        # 1. 初期化
        for line in init_code:
            f.write(line + "\n")
        
        lb_offset = 0

        # 2. ループ展開
        print(f"Generating {total_steps} steps...")
        for step in range(1, total_steps + 1):
            # 物理計算ブロック
            for line in physics_code:
                f.write(line + "\n")
            
            # ★条件変更: ステップ1 または 10の倍数のときに出力
            if step == 1 or step % 10 == 0:
                for line in energy_code_template:
                    if "l1bmm" in line:
                        f.write(line.format(lb_offset) + "\n")
                    else:
                        f.write(line + "\n")
                lb_offset += 16 # 書き込むたびにアドレスを進める

        # 3. 最終出力
        for line in final_output_code:
            f.write(line + "\n")

    print(f"Done! Generated: {filename}")
    print(f"Output logic: Step 1, 10, 20, 30... (Total {lb_offset // 16} outputs)")

if __name__ == "__main__":
    generate_vsm_final("1227_double_baneLJ.vsm", total_steps=2000)