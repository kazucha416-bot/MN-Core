def generate_mncore_skeleton(filename, loop_steps=10):
    # =================================================================
    #  1. ここにアセンブリコードをコピペしてください
    # =================================================================
    # ※ 変数 {lb_pe}, {lb_ke}, {lc} は自動で数値に置換されます。
    
    # --- 初期化ブロック (1回だけ実行) ---
    init_code = """
    # LM0の値セット
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

# ce,cf等係数の用意．後ほどこいつらが0番地に来るようにメモリ整理はします．．．
imm f"4.0" $lr64v # ce12
imm f"48.0" $lr72v # cf12
imm f"4.0" $ls8v # ce06
imm f"24.0" $ls16v # cf06
# 座標回転命令を使ってポジションの差を求める
# 1回転目
msr $lm0v $ls0v
nop
fvadd $lm0v -$ls0v $lr0v
# 2回転目
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr8v
# 3回転目
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr16v

# r^2を計算するために各要素の二乗を求める
fvmul $lr0v $lr0v $lr[24,32,40,48]
fvmul $lr8v $lr8v $lr[26,34,42,50]
fvmul $lr16v $lr16v $lr[28,36,44,52]
nop

fvpassa $lr24v $nowrite
fvadd $mauf $lr32v $nowrite
fvadd $mauf $lr40v $lr48v
nop
# 次はニュートンラフソン法でr2iを求める
frsqrt $lr48v $lr56v # lr56vに初期y0
imm f"0.5" $ls0v # ls0vに0.5
imm f"1.5" $ln8v # ln8vに1.5　のちのFMAの都合でlnに入れる必要あり
fvmul $lr56v $lr56v $nowrite # y0^2
fvmul $lr48v $mauf $nowrite # r2*y0^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y0^2
fvmul $lr56v $mauf $lr56v # y1 = y0 * (1.5 - 0.5*r2*y0^2)
nop
# NR法2回目
fvmul $lr56v $lr56v $nowrite # y1^2
fvmul $lr48v $mauf $nowrite # r2*y1^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y1^2
fvmul $lr56v $mauf $lr56v # y2 = y1 * (1.5 - 0.5*r2*y1^2)
nop
# NR法3回目
fvmul $lr56v $lr56v $nowrite # y2^2
fvmul $lr48v $mauf $nowrite # r2*y2^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y2^2
fvmul $lr56v $mauf $lr56v # y3 = y2 * (1.5 - 0.5*r2*y2^2)
nop
# NR法4回目
fvmul $lr56v $lr56v $nowrite # y3^2
fvmul $lr48v $mauf $nowrite # r2*y3^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y3^2
fvmul $lr56v $mauf $lr56v # y4 = y3 * (1.5 - 0.5*r2*y3^2)
nop
# r2i=y3^2をln8vに上書き格納
fvmul $lr56v $lr56v $ln8v
nop/2

fvmul $ln8v $ln8v $nowrite
fvmul $mauf $ln8v $nowrite
fvpassa $mauf $ln16v
nop/2
# ep = ce12 * r12i - ce06 * r06iを求める
fvfma $lr64v $ln16v -$ls8v $nowrite # ce12*r06i-ce06=nowrite
fvmul $mauf $ln16v $lm8v # mauf * r06i = ep
nop/2
l1bmm@0 $lm8v $lb{lb_pe} # この命令を使うとL1BMに12個のエネルギーが出力されるので，この合計を後ほど半分にすればよろしい．
# メモリは12ずつ増やすとする．



# fc = (cf12 * r12i - cf06 * r06i) * r2i 計算
fvfma $lr72v $ln16v -$ls16v $nowrite
fvmul $mauf $ln16v $nowrite
fvmul $mauf $ln8v $ls24v # fcがls24vに入る このあとlr0v~lr16vの座標と掛け算をするのでlsに格納
nop
# fx,fy,fzを求める fx = fc * x 
# ここが致命的に違う！！
fvmul $ls24 $lr0v $ls32v # fx
fvmul $ls26 $lr8v $ls40v # fy
fvmul $ls28 $lr16v $ls48v # fz
# 求めた力を足し合わせて，force1とする
fvpassa $ls40v $nowrite
fvadd $ls32v $mauf $nowrite
fvadd $mauf $ls48v $ls56v # ls56vにforce1が入った メモリ整理は後ほどやるが，fcはここでしか使わないので上書き格納していいかも
nop/2




# 初期速度での運動エネルギーを求める
fvmul $ln0v $ln0v $lr[0,8,16,24]
nop
fvpassa $lr8v $nowrite
fvadd $lr0v $mauf $nowrite
fvadd $lr16v $mauf $lr0v
imm f"0.5" $nowrite # m/2
fvmul $lr0v $aluf $lr0v # 運動エネルギー完成　lr0vに入る


# L1BMに入っているポテンシャルエネルギーをL2BMに転送
l2bm@0 $lb{lb_pe} $lc{lc}
# 空になったL1BMに運動エネルギーを転送
l1bmm@0 $lr0v $lb{lb_ke}
    """

    # --- ループブロック (loop_steps回 繰り返す) ---
    loop_code = """
    # 初期位置から求めた力と初期速度を使って位置の更新 pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5 * dt * dt / mas[j] * force1[0][j]
imm f"0.5" $lr0v #　係数
imm f"0.000001" $ls0v # h^2
imm f"1.0" $lr8v # 1/mass
fvmul $lr0v $ls0v $ls0v # 0.5 * h^2
fvmul $lr8v $ls56v $nowrite # (0.5 * h^2) * (1/mass) * force1
fvfma $ls0v $mauf $lm0v $ls0v #中間結果
imm f"0.001" $nowrite # h
fvfma $aluf $ln0v $ls0v $lm0v # pos = pos + h*v + (0.5*h^2/mass)*force1 更新完了



# 新しい位置での力を計算．さっきとやることは全く一緒．
# 座標回転命令を使ってポジションの差を求める
# 1回転目
nop/2
msr $lm0v $ls0v
nop
fvadd $lm0v -$ls0v $lr0v
# 2回転目
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr8v
# 3回転目
msr $ls0v $ls0v
nop
fvadd $lm0v -$ls0v $lr16v



# r^2を計算するために各要素の二乗を求める
fvmul $lr0v $lr0v $lr[24,32,40,48]
fvmul $lr8v $lr8v $lr[26,34,42,50]
fvmul $lr16v $lr16v $lr[28,36,44,52]
nop
# 足し合わせてr^2が求まる 
fvpassa $lr24v $nowrite
fvadd $mauf $lr32v $nowrite
fvadd $mauf $lr40v $lr48v
nop
# 次はニュートンラフソン法でr2iを求める
frsqrt $lr48v $lr56v # lr56vに初期y0
imm f"0.5" $ls0v # ls0vに0.5
imm f"1.5" $ln8v # ln8vに1.5　のちのFMAの都合でlnに入れる必要あり
fvmul $lr56v $lr56v $nowrite # y0^2
fvmul $lr48v $mauf $nowrite # r2*y0^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y0^2
fvmul $lr56v $mauf $lr56v # y1 = y0 * (1.5 - 0.5*r2*y0^2)
nop
# NR法2回目
fvmul $lr56v $lr56v $nowrite # y1^2
fvmul $lr48v $mauf $nowrite # r2*y1^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y1^2
fvmul $lr56v $mauf $lr56v # y2 = y1 * (1.5 - 0.5*r2*y1^2)
nop
# NR法3回目
fvmul $lr56v $lr56v $nowrite # y2^2
fvmul $lr48v $mauf $nowrite # r2*y2^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y2^2
fvmul $lr56v $mauf $lr56v # y3 = y2 * (1.5 - 0.5*r2*y2^2)
nop
# NR法4回目
fvmul $lr56v $lr56v $nowrite # y3^2
fvmul $lr48v $mauf $nowrite # r2*y3^2
fvfma $mauf -$ls0v $ln8v $nowrite # 1.5 - 0.5*r2*y3^2
fvmul $lr56v $mauf $lr56v # y4 = y3 * (1.5 - 0.5*r2*y3^2)
nop
# r2i=y3^2をln8vに上書き格納
fvmul $lr56v $lr56v $ln8v
nop/2
# r6iを求める = r2i^3 
fvmul $ln8v $ln8v $nowrite
fvmul $mauf $ln8v $nowrite
fvpassa $mauf $ln16v
nop/2
# ep = ce12 * r12i - ce06 * r06iを求める
fvfma $lr64v $ln16v -$ls8v $nowrite
fvmul $mauf $ln16v $lm8v
nop/2
l1bmm@0 $lm8v $lb{lb_pe} # メモリは16ずつ増やす


# fc = (cf12 * r12i - cf06 * r06i) * r2i 計算
fvfma $lr72v $ln16v -$ls16v $nowrite
fvmul $mauf $ln16v $nowrite
fvmul $mauf $ln8v $ls24v # fcがls24vに入る このあとlr0v~lr16vの座標と掛け算をするのでlsに格納
nop
# fx,fy,fzを求める fx = fc * x
fvmul $ls24 $lr0v $ls32v # fx
fvmul $ls26 $lr8v $ls40v # fy
fvmul $ls28 $lr16v $ls48v # fz

# 求めた力を足し合わせて，force2とする
fvpassa $ls40v $nowrite
fvadd $ls32v $mauf $nowrite
fvadd $mauf $ls48v $lr80v # lr80vにforce2が入った 後ほどf1+f2をするためlrに格納
nop/2

# Update Velocity v[0][j] = v[0][j] + 0.5 * dt / mas[j] * (force1[0][j] + force2[0][j])
imm f"0.5" $lr0v #　係数
imm f"0.001" $ls0v # h
imm f"1.0" $lr8v # 1/mass
fvmul $lr0v $ls0v $nowrite
fvmul $mauf $lr8v $lr0v
fvadd $ls56v $lr80v $nowrite
fvfma $mauf $lr0v $ln0v $ln0v # velocity更新完了
nop/2

# 運動エネルギーを求める
fvmul $ln0v $ln0v $lr[0,8,16,24]
nop
fvpassa $lr8v $nowrite
fvadd $lr0v $mauf $nowrite
fvadd $lr16v $mauf $lr0v
imm f"0.5" $nowrite # m/2
fvmul $lr0v $aluf $lr0v # 運動エネルギー完成　lr0vに入る

# L1BMに入っているポテンシャルエネルギーをL2BMに転送
l2bm@0 $lb{lb_pe} $lc{lc}
# 空になったL1BMに運動エネルギーを転送
l1bmm@0 $lr0v $lb{lb_ke}

fvpassa $lr80v $ls56v # force2を次のforce1へ．
    """

    # =================================================================
    #  2. メモリオフセット変数の初期値定義
    # =================================================================
    # 必要に応じて変更してください
    lb_pe_offset = 0
    lb_ke_offset = 0
    lc_offset    = 0

    # =================================================================
    #  3. 生成処理 (ここは触らなくてOK)
    # =================================================================
    
    def process_block(f, code_str, step_num=None):
        """コード文字列を行ごとに分割し、変数を埋め込んで書き込む"""
        lines = code_str.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # 変数埋め込み ({lb_pe}などを現在の数値に置換)
            # コメント行などはそのまま出力
            try:
                formatted_line = line.format(
                    lb_pe=lb_pe_offset,
                    lb_ke=lb_ke_offset,
                    lc=lc_offset
                )
                f.write(formatted_line + "\n")
            except IndexError:
                # {}が含まれていてformatに失敗した場合（アセンブリの記法と競合した場合など）
                # そのまま出力する
                f.write(line + "\n")

    with open(filename, "w") as f:
        f.write("# Generated MN-Core Code\n")

        # --- Init Block ---
        f.write("\n# === Initialization ===\n")
        process_block(f, init_code)
        
        # Initブロック終了後のオフセット更新 (必要なければ0にしてください)
        lb_pe_offset += 16
        lc_offset    += 16
        lb_ke_offset += 4

        # --- Loop Block ---
        print(f"Generating {loop_steps} loops...")
        for step in range(1, loop_steps + 1):
            f.write(f"\n# === Loop {step} ===\n")
            
            process_block(f, loop_code, step)
            
            # ループ1回ごとのオフセット更新
            lb_pe_offset += 16
            lc_offset    += 16
            lb_ke_offset += 4

        # --- Final Data Retrieval ---
        # 最後にデータを取得するコマンドを自動生成
        total_size_lb = lb_ke_offset  # ここまでの合計サイズ
        # total_size_lc = lc_offset   # 必要なら使う

        f.write("\n# === Final Data Retrieval ===\n")
        f.write(f"# Estimated size for KE buffer: {total_size_lb}\n")
        f.write(f"d getf $lb0n0c0b0 {total_size_lb}\n")
        f.write(f"d getf $lc0n0c0 {total_size_lb*4}\n")

    print(f"Generate Complete: {filename}")


# --- 実行 ---
if __name__ == "__main__":
    # 出力ファイル名とループ回数を指定
    generate_mncore_skeleton("FREEMD4_DEBUG_ACTUAL.vsm", loop_steps=500)