def generate_mncore_skeleton(filename, loop_steps=500, output_interval=50):
    # =================================================================
    #  1. アセンブリコード定義
    # =================================================================
    
    # --- 初期化ブロック (1回だけ実行) ---
    init_code = """
# 粒子0 
d set $lm0n0c0b0m0p0 4 0000000000000000000000000000000000000000000000000000000000000000
# 粒子1 
d set $lm0n0c0b0m0p1 4 00000000000000003f800000000000003f800000000000000000000000000000
# 粒子2
d set $lm0n0c0b0m0p2 4 3f800000000000003f8000000000000000000000000000000000000000000000
# 粒子3
d set $lm0n0c0b0m0p3 4 3f8000000000000000000000000000003f800000000000000000000000000000

# 粒子０の速度
d set $ln0n0c0b0m0p0 4 3f1fe4aa00000000bf964a6f00000000bfa21d01000000000000000000000000
# 粒子１の速度
d set $ln0n0c0b0m0p1 4 bfd34656000000003fb4457300000000be841a15000000000000000000000000
# 粒子２の速度
d set $ln0n0c0b0m0p2 4 3ed2590b00000000bf2e91bc000000003fcf9ae3000000000000000000000000
# 粒子３の速度
d set $ln0n0c0b0m0p3 4 3f1d7b7e000000003ee5376e00000000bdc77504000000000000000000000000

imm f"4.0" $lr64v # ce12
imm f"48.0" $lr72v # cf12
imm f"4.0" $ls8v # ce06
imm f"24.0" $ls16v # cf06
msr $lm0v $ls0v
nop
fvadd $lm0v -$ls0v $lr0v
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr8v
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr16v
fvmul $lr0v $lr0v $lr[24,32,40,48]
fvmul $lr8v $lr8v $lr[26,34,42,50]
fvmul $lr16v $lr16v $lr[28,36,44,52]
nop
fvpassa $lr24v $nowrite
fvadd $mauf $lr32v $nowrite
fvadd $mauf $lr40v $lr48v
nop
frsqrt $lr48v $lr56v
imm f"0.5" $ls0v
imm f"1.5" $ln8v
fvmul $lr56v $lr56v $nowrite
fvmul $lr48v $mauf $nowrite
fvfma $mauf -$ls0v $ln8v $nowrite
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $ln8v
nop/2
fvmul $ln8v $ln8v $nowrite
fvmul $mauf $ln8v $nowrite
fvpassa $mauf $ln16v
nop/2
fvfma $lr64v $ln16v -$ls8v $nowrite # ce12*r06i-ce06=nowrite
fvmul $mauf $ln16v $lm8v # mauf * r06i = ep
nop/2
l1bmm@0 $lm8v $lb{lb_pe} 
fvfma $lr72v $ln16v -$ls16v $nowrite
fvmul $mauf $ln16v $nowrite
fvmul $mauf $ln8v $ls24v 
nop
fvmul $ls24 $lr0v $ls32v # fx
fvmul $ls26 $lr8v $ls40v # fy
fvmul $ls28 $lr16v $ls48v # fz
fvpassa $ls40v $nowrite
fvadd $ls32v $mauf $nowrite
fvadd $mauf $ls48v $ls56v 
nop/2
fvmul $ln0v $ln0v $lr[0,8,16,24]
nop
fvpassa $lr8v $nowrite
fvadd $lr0v $mauf $nowrite
fvadd $lr16v $mauf $lr0v
imm f"0.5" $nowrite # m/2
fvmul $lr0v $aluf $lr0v 
l2bm@0 $lb{lb_pe} $lc{lc}
l1bmm@0 $lr0v $lb{lb_ke}
    """

    # --- ループコードの分割 ---
    
    # Part 1: 位置更新～相互作用計算（ポテンシャル出力直前まで）
    loop_part1 = """
imm f"0.5" $lr0v #　係数
imm f"0.000001" $ls0v # h^2
imm f"1.0" $lr8v # 1/mass
fvmul $lr0v $ls0v $ls0v # 0.5 * h^2
fvmul $lr8v $ls56v $nowrite # (0.5 * h^2) * (1/mass) * force1
fvfma $ls0v $mauf $lm0v $ls0v #中間結果
imm f"0.001" $nowrite # h
fvfma $aluf $ln0v $ls0v $lm0v # pos = pos + h*v + (0.5*h^2/mass)*force1 更新完了
nop/2
msr $lm0v $ls0v
nop
fvadd $lm0v -$ls0v $lr0v
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr8v
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr16v
fvmul $lr0v $lr0v $lr[24,32,40,48]
fvmul $lr8v $lr8v $lr[26,34,42,50]
fvmul $lr16v $lr16v $lr[28,36,44,52]
nop 
fvpassa $lr24v $nowrite
fvadd $mauf $lr32v $nowrite
fvadd $mauf $lr40v $lr48v
nop
frsqrt $lr48v $lr56v 
imm f"0.5" $ls0v 
imm f"1.5" $ln8v 
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $nowrite 
fvmul $lr48v $mauf $nowrite 
fvfma $mauf -$ls0v $ln8v $nowrite 
fvmul $lr56v $mauf $lr56v 
nop
fvmul $lr56v $lr56v $ln8v
nop/2
fvmul $ln8v $ln8v $nowrite
fvmul $mauf $ln8v $nowrite
fvpassa $mauf $ln16v
nop/2
"""

    # Part 2: ポテンシャルエネルギー計算と出力 (条件付き実行)
    loop_pe_output = """
# --- Potential Energy Output ---
fvfma $lr64v $ln16v -$ls8v $nowrite
fvmul $mauf $ln16v $lm8v
nop/2
l1bmm@0 $lm8v $lb{lb_pe}
# -----------------------------
"""

    # Part 3: 力の計算～速度更新（運動エネルギー出力直前まで）
    loop_part3 = """
fvfma $lr72v $ln16v -$ls16v $nowrite
fvmul $mauf $ln16v $nowrite
fvmul $mauf $ln8v $ls24v 
nop
fvmul $ls24 $lr0v $ls32v # fx
fvmul $ls26 $lr8v $ls40v # fy
fvmul $ls28 $lr16v $ls48v # fz
fvpassa $ls40v $nowrite
fvadd $ls32v $mauf $nowrite
fvadd $mauf $ls48v $lr80v 
nop/2
imm f"0.5" $lr0v 
imm f"0.001" $ls0v 
imm f"1.0" $lr8v 
fvmul $lr0v $ls0v $nowrite
fvmul $mauf $lr8v $lr0v
fvadd $ls56v $lr80v $nowrite
fvfma $mauf $lr0v $ln0v $ln0v # velocity更新完了
nop/2
"""

    # Part 4: 運動エネルギー計算と出力 (条件付き実行)
    loop_ke_output = """
# --- Kinetic Energy Output ---
fvmul $ln0v $ln0v $lr[0,8,16,24]
nop
fvpassa $lr8v $nowrite
fvadd $lr0v $mauf $nowrite
fvadd $lr16v $mauf $lr0v
imm f"0.5" $nowrite # m/2
fvmul $lr0v $aluf $lr0v 
l2bm@0 $lb{lb_pe} $lc{lc}
l1bmm@0 $lr0v $lb{lb_ke}
# ---------------------------
"""

    # Part 5: ループの締めくくり
    loop_part5 = """
fvpassa $lr80v $ls56v # force2を次のforce1へ．
"""

    # =================================================================
    #  2. メモリオフセット変数の初期値定義
    # =================================================================
    lb_pe_offset = 0
    lb_ke_offset = 0
    lc_offset    = 0

    # =================================================================
    #  3. 生成処理
    # =================================================================
    
    def process_block(f, code_str):
        """コード文字列を行ごとに分割し、変数を埋め込んで書き込む"""
        lines = code_str.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            try:
                formatted_line = line.format(
                    lb_pe=lb_pe_offset,
                    lb_ke=lb_ke_offset,
                    lc=lc_offset
                )
                f.write(formatted_line + "\n")
            except (IndexError, ValueError):
                f.write(line + "\n")

    with open(filename, "w") as f:
        f.write("# Generated MN-Core Code\n")

        # --- Init Block ---
        f.write("\n# === Initialization ===\n")
        process_block(f, init_code)
        
        # Initブロック終了後のオフセット更新 (ここは1回目なので必ず進める)
        lb_pe_offset += 16
        lc_offset    += 16
        lb_ke_offset += 4

        # --- Loop Block ---
        print(f"Generating {loop_steps} loops with output every {output_interval} steps...")
        
        for step in range(1, loop_steps + 1):
            f.write(f"\n# === Loop {step} ===\n")
            
            # 1. 物理演算前半（常に出力）
            process_block(f, loop_part1)
            
            # 2. ポテンシャルエネルギー出力 (50回に1回)
            if step % output_interval == 0:
                process_block(f, loop_pe_output)
            
            # 3. 物理演算中盤（常に出力）
            process_block(f, loop_part3)
            
            # 4. 運動エネルギー出力 & オフセット更新 (50回に1回)
            if step % output_interval == 0:
                process_block(f, loop_ke_output)
                
                # ★ここが重要：出力した時だけメモリの場所を進める
                lb_pe_offset += 16
                lc_offset    += 16
                lb_ke_offset += 4
            
            # 5. ループの締め（常に出力）
            process_block(f, loop_part5)

        # --- Final Data Retrieval ---
        total_size_lb = lb_ke_offset
        f.write("\n# === Final Data Retrieval ===\n")
        f.write(f"# Estimated size for KE buffer: {total_size_lb}\n")
        # 500stepで50回に1回なら、約10回分のデータ量になるはずなので安全
        f.write(f"d getf $lb0n0c0b0 {total_size_lb}\n")
        f.write(f"d getf $lc0n0c0 {total_size_lb*4}\n")

    print(f"Generate Complete: {filename}")


# --- 実行 ---
if __name__ == "__main__":
    # 出力ファイル名とループ回数を指定
    # 例：500ステップ回して、50ステップごとにエネルギーを出力
    generate_mncore_skeleton("Shin_Freemd4_MNCORE.vsm", loop_steps=3000, output_interval=10)