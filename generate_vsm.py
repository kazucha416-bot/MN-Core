def generate_lj_kernel(loops):
    code = []
    
    for i in range(loops):
        # レジスタ番号計算
        lm = f"$lm{i * 2}"
        ln = f"$ln{i * 2}"
        lr_a = f"$lr{2 + (i * 4)}"
        lr_b = f"$lr{4 + (i * 4)}"

        # 純粋なコードブロック (コメントなし)
        block = f"""frsqrt {lm} {lr_a}
nop/2
fvmul {lr_a} {lr_a} $nowrite
fvmul {lm} $mauf $nowrite
fvfma $mauf -$ls0 $lr0 $nowrite
fvmul {lr_a} $mauf {lr_a}
nop/2
fvmul {lr_a} {lr_a} $nowrite
fvmul {lm} $mauf $nowrite
fvfma $mauf -$ls0 $lr0 $nowrite
fvmul {lr_a} $mauf {lr_a}
nop/2
fvmul {lr_a} {lr_a} $nowrite
fvmul {lm} $mauf $nowrite
fvfma $mauf -$ls0 $lr0 $nowrite
fvmul {lr_a} $mauf {lr_a}
nop/2
fvmul {lr_a} {lr_a} $nowrite
fvmul {lm} $mauf $nowrite
fvfma $mauf -$ls0 $lr0 $nowrite
fvmul {lr_a} $mauf {lr_a}
nop/2
fvmul {lr_a} {lr_a} $nowrite
fvmul $mauf $mauf {lr_a}
nop/2
fvmul {lr_a} {lr_a} $nowrite
fvmul $mauf {lr_a} {lr_b}
nop
imm f"48.0" $nowrite
fvfma $aluf {lr_b} -$ls2 $nowrite
fvmul $mauf {lr_b} $nowrite
fvmul $mauf {lr_a} $nowrite
fvmul $mauf {lm} {ln}"""
        code.append(block)

    return "\n".join(code)

if __name__ == "__main__":
    # 生成したいループ回数を指定
    num_loops = 61 # ピッタリこのループ分プロットを出せることになる．
    
    generated_code = generate_lj_kernel(num_loops)
    
    # ファイルに保存 (コンソール出力なし)
    filename = "generated_kernel.vsm"
    with open(filename, "w") as f:
        f.write(generated_code)