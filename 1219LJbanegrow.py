import os
# 1226　N法の回数を４回に変更．単精度に合わせるのと，卒論的に４回でやった方が都合がよい．
def main():
    # 設定
    filepath = "/home/kazuki/mncore/baneljdouble_sparse_compact.vsm"
    loop_count = 2000
    interval = 50
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    print(f"2粒子LJ問題倍精度（軽量化版・{interval}step出力）を {filepath} に書き出します...")

    output_count = 0

    with open(filepath, "w") as f:
        # --- 1. 初期化ブロック (コメント・空行削除) ---
        f.write("""
# x-1.3 h=0.001 m=1 ε=1 σ=1 1/m=1 h^2=1e-6
d set $lm0n0c0b0m0p0 7 3ff4cccccccccccd3f50624dd2f1a9fc3ff00000000000003ff00000000000003ff00000000000003ff00000000000003eb0c6f7a0b5ed8d
# v0=0.0 h^2=1e-6 0.5 for Newton-Raphson
d set $ln0n0c0b0m0p0 3 00000000000000003eb0c6f7a0b5ed8d3fe0000000000000
# ce06=4 ce12=4
d set $lr0n0c0b0m0p0 2 40100000000000004010000000000000
# cf06=24 cf12=48 1.5 for Newton-Raphson
d set $ls0n0c0b0m0p0 3 403800000000000040480000000000003ff8000000000000

drsqrt $lm0 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $nowrite
dvmulu $mauf $mauf $lr8
nop/2
dvmulu $lr8 $lr8 $nowrite
dvmulu $mauf $lr8 $lr10
nop/2
dvmulu $lr10 $lr10 $lr12
nop
dvmulu $ls0 $lr10 $nowrite
dvfmau $ls2 $lr12 -$mauf $nowrite
dvmulu $mauf $lr8 $ls8
nop/2
dvmulu $ls8 $lm0 $ls10
dvmulu $ln2 $lm12 $lr14
nop
dvmulu $ls10 $lm10 $ls12
""")

        # --- 2. ループ部分 ---
        for k in range(loop_count):
            # 物理計算ループ
            f.write("""nop/2
dvfmau $lr14 $ls12 $lm0 $nowrite
dvfmau $lm2 $ln0 $mauf $nowrite
dvpassa $mauf $lm0
nop/2
drsqrt $lm0 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $ls6
nop/2
dvmulu $lm0 $ls6 $lr6
nop/2
dvfmau $lr6 -$ln4 $ls4 $nowrite
dvmulu $mauf $lr4 $lr4
nop/2
dvmulu $lr4 $lr4 $nowrite
dvmulu $mauf $mauf $lr8
nop/2
dvmulu $lr8 $lr8 $nowrite
dvmulu $mauf $lr8 $lr10
nop/2
dvmulu $lr10 $lr10 $lr12
nop
dvmulu $ls0 $lr10 $nowrite
dvfmau $ls2 $lr12 -$mauf $nowrite
dvmulu $mauf $lr8 $ls8
nop/2
dvmulu $ls8 $lm0 $lr16
dvmulu $ln4 $lm2 $lr18
nop
dvadd $ls10 $lr16 $nowrite
dvmulu $mauf $lm10 $nowrite
dvfmau $mauf $lr18 $ln0 $ln0
dvpassa $lr16 $ls10
""")

            # エネルギー出力 (50 stepに1回)
            if k % interval == 0:
                lb_addr = output_count * 4
                f.write(f"""dvpassa $lr2 $nowrite
dvmulu $mauf $lr12 $ls20
nop
dvpassa $lr10 $nowrite
dvfmau $mauf -$lr0 $ls20 $lm14
nop/2
dvmulu $ln4 $lm4 $lr22
nop
dvmulu $ln0 $ln0 $nowrite 
dvmulu $mauf $lr22 $lm16
nop/2
dvpassa $lm16 $nowrite
dvadd $mauf $lm14 $nowrite
dvpassa $mauf $lm18
nop/2
l1bmm@0 $lm18 $lb{lb_addr}
""")
                output_count += 1

        # --- 3. 終了処理 ---
        l1bm_size = output_count * 4
        f.write(f"""d getd $lm0n0c0b0 m0p0 10
d getd $ln0n0c0b0m0p0 4
d getd $lr0n0c0b0m0p0 12
d getd $ls0n0c0b0m0p0 8
d getd $lb0n0c0b0 {l1bm_size+1}
""")

    print(f"完了しました。L1BM出力サイズ: {l1bm_size+1}")

if __name__ == "__main__":
    main()