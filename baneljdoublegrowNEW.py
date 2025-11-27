import os

def main():
    # --- 設定 ---
    filepath = "/home/kazuki/mncore/baneljdouble.vsm"
    loop_count = 2000   # 2000ステップ回す
    skip_step = 10      # 10ステップに1回保存
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    print(f"倍精度アセンブリコード(間引き保存版)を {filepath} に書き出します...")

    # 保存した回数をカウントする変数
    save_count = 0

    with open(filepath, "w") as f:
        # --- 1. 初期化ブロック (共通) ---
        f.write("""
d set $lm0n0c0b0m0p0 5 3ff4cccccccccccd3f50624dd2f1a9fc3ff00000000000003ff00000000000003ff0000000000000
d set $ln0n0c0b0m0p0 2 00000000000000003eb0c6f7a0b5ed8d
d set $ls18n0c0b0m0p0 1 3fe0000000000000
d set $lr20n0c0b0m0p0 1 4010000000000000
dvmulu $lm8 $lm8 $nowrite
dvmulu $mauf $lm8 $nowrite
dvmulu $mauf $mauf $lr0
dvmulu $lr20 $lm6 $ls0
nop
dvmulu $lr0 $lr0 $lr2
dvmulu $ls0 $lr0 $lr0
nop/2
dvmulu $ls0 $lr2 $lr2
immu i"0x40180000" $nowrite
dvmulu $aluf $lr0 $ls0
immu i"0x40280000" $nowrite
dvmulu $aluf $lr2 $ls2

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
dvmulu $mauf $lr6 $ls8
nop/2
dvmulu $ls8 $lm0 $ls10

drsqrt $lm4 $nowrite
dvmulu $aluf $aluf $ls4
nop
immu i"0x40000000" $nowrite
dvfmau $lm4 -$ls4 $aluf $nowrite
nop/2
dvmulu $ls4 $mauf $lm10 $ls4
nop
immu i"0x40000000" $nowrite
dvfmau $lm4 -$ls4 $aluf $nowrite
nop/2
dvmulu $ls4 $mauf $lm10 $ls4
nop/2
dvmulu $lm10 $ls10 $ls12

dvmulu $ln2 $ls18 $lr12

dvpassa $lm2 $lr14

""")

        # --- 2. ループ部分 ---
        for k in range(loop_count):
            # 計算部分は毎ステップ出力
            f.write(f"""# Loop {k}
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

""")
            
            # ★ここが変更点: 10回に1回だけ保存命令を出力
            if k % skip_step == 0:
                # アドレスは「保存した回数」に基づいて計算 (1回につき16増える)
                base_addr = save_count * 16
                
                f.write(f"""l1bmm@0 $mauf $lb{base_addr}      # TotalE
l1bmm@0 $lm0 $lb{base_addr + 4}   # Pos
l1bmm@0 $lm12 $lb{base_addr + 8}  # PE
l1bmm@0 $lm14 $lb{base_addr + 12} # KE

""")
                save_count += 1  # 保存回数をカウントアップ

        # --- 3. 終了ブロック ---
        # 最後のデータサイズは 保存回数 * 16
        total_data_size = save_count * 16
        
        f.write(f"""
d getd $lm0n0c0b0m0p0 20
d getd $ln0n0c0b0m0p0 2
d getd $lr0n0c0b0m0p0 20
d getd $ls0n0c0b0m0p0 20
d getd $lb0n0c0b0 {total_data_size}
""")

    print(f"完了しました。 (保存回数: {save_count}回, L1BM使用量: {total_data_size}語)")

if __name__ == "__main__":
    main()
