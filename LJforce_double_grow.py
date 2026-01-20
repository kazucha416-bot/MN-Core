def generate_lj_kernel(loops):
    code = []
    
    for i in range(loops):
        # レジスタ番号計算
        lm = f"$lm{i * 2}"
        ln = f"$ln{i * 2}"
        lr_a = f"$lr{2 + (i * 4)}"
        lr_b = f"$lr{4 + (i * 4)}"

        # 純粋なコードブロック (コメントなし)
        block = f"""drsqrt {lm} {lr_a}
nop/2
dvmulu {lr_a} {lr_a} $nowrite
dvmulu {lm} $mauf $nowrite
dvfmau $mauf -$ls0 $lr0 $nowrite
dvmulu {lr_a} $mauf {lr_a}
nop/2
dvmulu {lr_a} {lr_a} $nowrite
dvmulu {lm} $mauf $nowrite
dvfmau $mauf -$ls0 $lr0 $nowrite
dvmulu {lr_a} $mauf {lr_a}
nop/2
dvmulu {lr_a} {lr_a} $nowrite
dvmulu {lm} $mauf $nowrite
dvfmau $mauf -$ls0 $lr0 $nowrite
dvmulu {lr_a} $mauf {lr_a}
nop/2
dvmulu {lr_a} {lr_a} $nowrite
dvmulu {lm} $mauf $nowrite
dvfmau $mauf -$ls0 $lr0 $nowrite
dvmulu {lr_a} $mauf {lr_a}
nop/2
dvmulu {lr_a} {lr_a} $nowrite
dvmulu $mauf $mauf {lr_a}
nop/2
dvmulu {lr_a} {lr_a} $nowrite
dvmulu $mauf {lr_a} {lr_b}
nop/2
dvfmau $lm1024 {lr_b} -$ls2 $nowrite
dvmulu $mauf {lr_b} $nowrite
dvmulu $mauf {lr_a} $nowrite
dvmulu $mauf {lm} {ln}"""
        code.append(block)

    return "\n".join(code)

if __name__ == "__main__":
    # 生成したいループ回数を指定
    num_loops = 61 # ピッタリこのループ分プロットを出せることになる．
    
    generated_code = generate_lj_kernel(num_loops)
    
    # ファイルに保存 (コンソール出力なし)
    filename = "LJforce_double.vsm"
    with open(filename, "w") as f:
        f.write(generated_code)