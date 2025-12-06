import os

def main():
    # 設定
    filepath = "/home/kazuki/mncore/baneljdouble.vsm"
    loop_count = 2
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    print(f"倍精度アセンブリコードを {filepath} に書き出します...")

    with open(filepath, "w") as f:
        # --- 1. 初期化ブロック ---
        f.write("""
d set $lm0n0c0b0m0p0 6 3ff4cccccccccccd3f50624dd2f1a9fc3ff00000000000003ff00000000000003ff00000000000003ff0000000000000
d set $ln0n0c0b0m0p0 2 00000000000000003eb0c6f7a0b5ed8d
d set $lr0n0c0b0m0p0 2 40100000000000004010000000000000
d set $ls0n0c0b0m0p0 2 40380000000000004048000000000000


drsqrt $lm0 $lr4
dvmulu $lr4 $lr4 $ls4
dvmulu $lm0 $ls4 $lr6
dvfmau $lr6 -$ln4 $ls6 $ls8
dvmulu $ls8 $lr4 $lr8 $lr4
""")

        # --- 2. ループ部分 ---
        for k in range(loop_count):
            # ★修正: 倍精度でも L1BMアドレス単位は長語かつ4長語アライン必須なので、増加は 4 のまま
            lb_addr = k * 4
            
            f.write(f"""#ここからループ開始
dvpassa $ln0 $ls14
nop/2
dvfmau $lr14 $ls14 $lm0 $nowrite
dvfmau $lr12 $ls12 $mauf $lm0
nop/2
dvmulu $lm0 $lm0 $lr4
nop/2
drsqrt $lr4 $nowrite
dvmulu $aluf $aluf $ls4
nop
immu i"0x40000000" $nowrite
dvfmau $lr4 -$ls4 $aluf $nowrite
nop/2
dvmulu $ls4 $mauf $lr6 $ls4
nop
immu i"0x40000000" $nowrite
dvfmau $lr4 -$ls4 $aluf $nowrite
nop/2
dvmulu $ls4 $mauf $lr6 $ls4
nop/2

dvmulu $lr6 $lr6 $ls6
nop/2
dvmulu $lr6 $ls6 $lr8
nop/2
dvmulu $lr8 $lr8 $lr10
nop
dvmulu $ls0 $lr8 $nowrite
dvfmau $ls2 $lr10 -$mauf $nowrite
dvmulu $mauf $lr6 $ls16
nop/2
dvmulu $ls16 $lm0 $lr16
dvmulu $ls18 $lm2 $lr20
nop
dvadd $ls10 $lr16 $nowrite
dvfmau $mauf $lr20 $ln0 $ln0
dvpassa $lr16 $ls10
dvpassa $lr8 $nowrite
dvmulu $mauf $lr0 $ls20
dvpassa $lr10 $nowrite
nop
dvfmau $lr2 $mauf -$ls20 $lm12
nop/2
dvmulu $ls18 $lm4 $lr20
nop/2
dvmulu $ln0 $ln0 $nowrite
nop/2
dvmulu $mauf $lr20 $lm14
nop/2
dvpassa $lm14 $nowrite
dvadd $mauf $lm12 $nowrite
l1bmm@0 $mauf $lb{lb_addr}

""")

        # --- 3. 終了ブロック ---
        # ★修正: サイズも 4 * loop_count に戻します
        f.write(f"""
d getd $lm0n0c0b0m0p0 20
d getd $ln0n0c0b0m0p0 2
d getd $lr0n0c0b0m0p0 20
d getd $ls0n0c0b0m0p0 20
d getd $lb0n0c0b0 {4 * loop_count}
""")

    print("完了しました。")

if __name__ == "__main__":
    main()
