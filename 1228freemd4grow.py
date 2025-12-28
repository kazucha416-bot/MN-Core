def generate_4particle_vsm_final(filename, loop_steps=10):
    # ==========================================
    # 1. 初期化ブロック
    # ==========================================
    init_template = [
        "# 1228 4-Particle MD - Initialization",
        "d set $lm0n0c0b0m0p0 4 0000000000000000000000000000000000000000000000000000000000000000",
        "d set $lm0n0c0b0m0p1 4 00000000000000003f800000000000003f800000000000000000000000000000",
        "d set $lm0n0c0b0m0p2 4 3f800000000000003f8000000000000000000000000000000000000000000000",
        "d set $lm0n0c0b0m0p3 4 3f8000000000000000000000000000003f800000000000000000000000000000",
        "d set $ln0n0c0b0m0p0 4 3fb7f6db000000003f1201b8000000003f070790000000000000000000000000",
        "d set $ln0n0c0b0m0p1 4 bf8c2185000000003ea5e61000000000bf8b5336000000000000000000000000",
        "d set $ln0n0c0b0m0p2 4 bd83ffa0000000003f9b231d00000000be9edb8a000000000000000000000000",
        "d set $ln0n0c0b0m0p3 4 be8e556e00000000c006cebf000000003f5f0ca1000000000000000000000000",
        "imm f\"4.0\" $lr64v",
        "imm f\"48.0\" $lr72v",
        "imm f\"4.0\" $ls8v",
        "imm f\"24.0\" $ls16v",
        "msr $lm0v $ls0v",
        "nop",
        "fvadd $lm0v -$ls0v $lr0v",
        "msr $ls0v $ls0v",
        "nop",
        "fvadd $lm0v -$ls0v $lr8v",
        "msr $ls0v $ls0v",
        "nop",
        "fvadd $lm0v -$ls0v $lr16v",
        "fvmul $lr0v $lr0v $lr[24,32,40,48]",
        "fvmul $lr8v $lr8v $lr[26,34,42,50]",
        "fvmul $lr16v $lr16v $lr[28,36,44,52]",
        "nop",
        "fvpassa $lr24v $nowrite",
        "fvadd $mauf $lr32v $nowrite",
        "fvadd $mauf $lr40v $lr48v",
        "nop",
        "frsqrt $lr48v $lr56v",
        "imm f\"0.5\" $ls0v",
        "imm f\"1.5\" $ln8v",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $ln8v",
        "nop/2",
        "fvmul $ln8v $ln8v $nowrite",
        "fvmul $mauf $ln8v $nowrite",
        "fvpassa $mauf $ln16v",
        "nop/2",
        "fvfma $lr64v $ln16v -$ls8v $nowrite",
        "fvmul $mauf $ln16v $lm8v",
        "nop/2",
        "l1bmm@0 $lm8v $lb{lb_pe}",
        "fvfma $lr72v $ln16v -$ls16v $nowrite",
        "fvmul $mauf $ln16v $nowrite",
        "fvmul $mauf $ln8v $ls24v",
        "nop",
        "fvmul $ls24v $lr0v $ls32v",
        "fvmul $ls24v $lr8v $ls40v",
        "fvmul $ls24v $lr16v $ls48v",
        "fvpassa $ls40v $nowrite",
        "fvadd $ls32v $mauf $nowrite",
        "fvadd $mauf $ls48v $ls56v",
        "nop/2",
        "fvmul $ln0v $ln0v $lr[0,8,16,24]",
        "nop",
        "fvpassa $lr8v $nowrite",
        "fvadd $lr0v $mauf $nowrite",
        "fvadd $lr16v $mauf $lr0v",
        "imm f\"0.5\" $nowrite",
        "fvmul $lr0v $aluf $lr0v",
        "l2bm@0 $lb{lb_pe} $lc{lc}",
        "l1bmm@0 $lr0v $lb{lb_ke}"
    ]

    # ==========================================
    # 2. ループブロック
    # ==========================================
    loop_template = [
        "imm f\"0.5\" $lr0v",
        "imm f\"0.000001\" $ls0v",
        "imm f\"1.0\" $lr8v",
        "fvmul $lr0v $ls0v $ls0v",
        "fvmul $lr8v $ls56v $nowrite",
        "fvfma $ls0v $mauf $lm0v $ls0v",
        "imm f\"0.001\" $nowrite",
        "fvfma $aluf $ln0v $ls0v $lm0v",
        "nop/2",
        "msr $lm0v $ls0v",
        "nop",
        "fvadd $lm0v -$ls0v $lr0v",
        "msr $ls0v $ls0v",
        "nop",
        "fvadd $lm0v -$ls0v $lr8v",
        "msr $ls0v $ls0v",
        "nop",
        "fvadd $lm0v -$ls0v $lr16v",
        "fvmul $lr0v $lr0v $lr[24,32,40,48]",
        "fvmul $lr8v $lr8v $lr[26,34,42,50]",
        "fvmul $lr16v $lr16v $lr[28,36,44,52]",
        "nop",
        "fvpassa $lr24v $nowrite",
        "fvadd $mauf $lr32v $nowrite",
        "fvadd $mauf $lr40v $lr48v",
        "nop",
        "frsqrt $lr48v $lr56v",
        "imm f\"0.5\" $ls0v",
        "imm f\"1.5\" $ln8v",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $nowrite",
        "fvmul $lr48v $mauf $nowrite",
        "fvfma $mauf -$ls0v $ln8v $nowrite",
        "fvmul $lr56v $mauf $lr56v",
        "nop",
        "fvmul $lr56v $lr56v $ln8v",
        "nop/2",
        "fvmul $ln8v $ln8v $nowrite",
        "fvmul $mauf $ln8v $nowrite",
        "fvpassa $mauf $ln16v",
        "nop/2",
        "fvfma $lr64v $ln16v -$ls8v $nowrite",
        "fvmul $mauf $ln16v $lm8v",
        "nop/2",
        "l1bmm@0 $lm8v $lb{lb_pe}",
        "fvfma $lr72v $ln16v -$ls16v $nowrite",
        "fvmul $mauf $ln16v $nowrite",
        "fvmul $mauf $ln8v $ls24v",
        "nop",
        "fvmul $ls24v $lr0v $ls32v",
        "fvmul $ls24v $lr8v $ls40v",
        "fvmul $ls24v $lr16v $ls48v",
        "fvpassa $ls40v $nowrite",
        "fvadd $ls32v $mauf $nowrite",
        "fvadd $mauf $ls48v $lr80v",
        "nop/2",
        "imm f\"0.5\" $lr0v",
        "imm f\"0.001\" $ls0v",
        "imm f\"1.0\" $lr8v",
        "fvmul $lr0v $ls0v $nowrite",
        "fvmul $mauf $lr8v $lr0v",
        "fvadd $ls56v $lr80v $nowrite",
        "fvfma $mauf $lr0v $ln0v $ln0v",
        "nop/2",
        "fvmul $ln0v $ln0v $lr[0,8,16,24]",
        "nop",
        "fvpassa $lr8v $nowrite",
        "fvadd $lr0v $mauf $nowrite",
        "fvadd $lr16v $mauf $lr0v",
        "imm f\"0.5\" $nowrite",
        "fvmul $lr0v $aluf $lr0v",
        "l2bm@0 $lb{lb_pe} $lc{lc}",
        "l1bmm@0 $lr0v $lb{lb_ke}",
        "fvpassa $lr80v $ls56v"
    ]

    with open(filename, 'w') as f:
        # --- アドレスカウンタ初期化 ---
        lb_pe_offset = 0  # PE用 (16ずつ増加)
        lb_ke_offset = 0  # KE用 (4ずつ増加)
        lc_offset = 0     # LC用 (16ずつ増加)

        # --- Init Block ---
        for line in init_template:
            if line.strip().startswith("#"): continue
            
            code_line = line.format(
                lb_pe=lb_pe_offset,
                lb_ke=lb_ke_offset,
                lc=lc_offset
            )
            f.write(code_line + "\n")
        
        # Init完了後のカウンタ更新
        lb_pe_offset += 16
        lc_offset    += 16
        lb_ke_offset += 4

        # --- Loop Block ---
        print(f"Generating {loop_steps} loops with Final Output...")
        for step in range(1, loop_steps + 1):
            for line in loop_template:
                if line.strip().startswith("#"): continue
                
                code_line = line.format(
                    lb_pe=lb_pe_offset,
                    lb_ke=lb_ke_offset,
                    lc=lc_offset
                )
                f.write(code_line + "\n")
            
            # ループごとのカウンタ更新
            lb_pe_offset += 16
            lc_offset    += 16
            lb_ke_offset += 4

        # ==========================================
        # 3. 最終出力 (d getf)
        # ==========================================
        # サイズ計算: (ループ回数 + 初期化1回) * 単位サイズ
        total_steps = loop_steps + 1
        size_lb = 4 * total_steps  # KE用 (4 word/step)
        size_lc = 16 * total_steps # PE用 (16 word/step)

        f.write(f"d getf $lb0n0c0b0 {size_lb}\n")
        f.write(f"d getf $lc0n0c0 {size_lc}\n")

    print(f"Done! Generated: {filename}")
    print(f"Loop Steps: {loop_steps}")
    print(f"Output Size -> LB(KE): {size_lb}, LC(PE): {size_lc}")

if __name__ == "__main__":
    generate_4particle_vsm_final("1228_4particle_float.vsm", loop_steps=500)