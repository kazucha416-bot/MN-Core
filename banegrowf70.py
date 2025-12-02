def main():
    filename = "banemasunew.vsm"
    
    # 設定
    max_loop = 70       # ループ回数
    output_interval = 10 # 何ステップごとに保存するか (10回に1回)

    print(f"VSMファイルを生成します: {filename}")

    with open(filename, "w") as f:
        # --- 初期化部分 ---
        # d set で初期値を設定 (h=0.1, x0=1.0, v0=0, etc...)
        # 長い16進数はそのまま記述します
        f.write("d set $lm0n0c0b0m0p0 10 3DCCCCCD000000000000000000000000000000000000000000000000000000003F800000000000000000000000000000000000000000000000000000000000003F000000000000000000000000000000\n")
        f.write('imm f"1.0" $ls0v/1000 #x0=1.0\n')
        f.write('imm f"0" $lr0v #v0=0\n')
        f.write("\n")

        lb_addr = 0  # $lb の書き込み先アドレス

        # --- 繰り返し部分 ---
        for i in range(1, max_loop + 1):
            # 1. オイラー法による更新 (これは毎ステップ実行)
            f.write("fvmul -$lm8v $ls0v $nowrite\n")
            f.write(f"fvfma $ls256v $lm0v $lr0v $lr0v #v({i})\n")
            f.write("nop\n")
            f.write(f"fvfma $lr0v $lm0v $ls0v $ls0v #x({i})\n")
            f.write("nop\n")

            # 2. エネルギー計算とL1BMへの転送 (10ステップに1回だけ実行)
            if i % output_interval == 0:
                # エネルギー計算
                f.write("fvmul $lr0v $lr0v $lr64v\n")      # v^2
                f.write("fvmul $ls0v $ls0v $nowrite\n")    # x^2 (結果はmaufへ)
                f.write("nop\n")
                f.write("fvadd $lr64v $mauf $nowrite\n")   # v^2 + x^2
                f.write("nop/2\n")
                f.write("fvmul $lm16v $mauf $nowrite\n")   # 0.5 * (v^2 + x^2)
                
                # L1BMに書き込み
                f.write(f"l1bmm@0 $mauf $lb{lb_addr}\n")
                
                # アドレスを4増やす (書き込んだ時だけ増やす)
                lb_addr += 4
            
            f.write("\n") # 可読性のため改行

        # --- 終了処理 ---
        # 最後の出力サイズ (実際に書き込んだ量 = lb_addr)
        f.write(f"d getf $lb0n0c0b0 {lb_addr}\n")
        f.write("d getf $lm0n0c0b0m0p0 16\n")

    print("完了しました。")

if __name__ == "__main__":
    main()
