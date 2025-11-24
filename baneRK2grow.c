#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp;
    // 出力先ファイルパス (必要に応じて変更してください)
    const char *filepath = "/home/kazuki/mncore/baneRK2new.vsm";
    int loop_count = 70; // 繰り返す回数

    // ファイルを開く (書き込みモード)
    fp = fopen(filepath, "w");
    if (fp == NULL) {
        printf("エラー: ファイル %s を開けません。\n", filepath);
        exit(1);
    }

    printf("アセンブリコードを %s に書き出します...\n", filepath);

    // --- 1. 初期化コード (1回だけ出力) ---
    fprintf(fp, "#２次のルンゲクッタ\n");
    // 初期位置 x=1.0 (3f800000)
    fprintf(fp, "d set $lm0n0c0b0m0p0 1 3f8000003f800000\n");
    // 初期速度 v=0.0 (00000000)
    fprintf(fp, "d set $ln0n0c0b0m0p0 1 0000000000000000\n");
    // 定数テーブル: k(1.0), dt(0.1), 0.5*dt(0.05), 0.5(0.5)
    fprintf(fp, "d set $ls0n0c0b0m0p0 4 3f8000003f8000003dcccccd3dcccccd3d4ccccd3d4ccccd3f0000003f000000\n");
    fprintf(fp, "\n");

    // --- 2. 計算ループ (loop_count回出力) ---
    for (int k = 0; k < loop_count; k++) {
        // Step 1: k1の計算 (k1v = -k*x, k1x = v)
        // mauf = -k($ls0) * x($lm0)
        fprintf(fp, "fvmul -$ls0 $lm0 $nowrite\n"); 
        
        // x_mid = x + k1x($ln0) * 0.5dt($ls4) -> $lr2
        fprintf(fp, "fvfma $mauf $ls4 $ln0 $lr2\n");
        
        // Step 2: 中点での計算準備
        // mauf = v($ln0) * 0.5dt($ls4) + x($lm0) (これ計算順序的に怪しいかも？ v_mid計算の準備？)
        // 元コード: fvfma $ln0 $ls4 $lm0 $nowrite -> x + v*0.5dt を計算してmaufへ
        fprintf(fp, "fvfma $ln0 $ls4 $lm0 $nowrite\n");
        
        // k2v = -k($ls0) * x_mid($lr2? いやmaufに入ってるx_mid相当を使う想定？)
        // 元コード: fvmul $mauf -$ls0 $lr4 -> $lr4 = k2v (-k * x_mid)
        fprintf(fp, "fvmul $mauf -$ls0 $lr4\n");
        
        // Step 3: 更新 (Update)
        // x_new = x_mid($lr2?いやk1x*0.5dt) * dt($ls2)? 
        // 元コード: fvfma $lr2 $ls2 $lm0 $lm0 -> x_new = x + v_mid * dt ではなく、変な更新に見える
        // 恐らく $lr2 は v_mid で、$lm0(x) に $ls2(dt) * $lr2(v_mid) を足している？
        fprintf(fp, "fvfma $lr2 $ls2 $lm0 $lm0\n");
        fprintf(fp, "nop\n");
        
        // v_new = v($ln0) + k2v($lr4) * dt($ls2)
        fprintf(fp, "fvfma $lr4 $ls2 $ln0 $ln0\n");
        fprintf(fp, "nop\n");
        
        // エネルギー計算 (Total E = 0.5*x^2 + 0.5*v^2)
        // x^2
        fprintf(fp, "fvmul $lm0 $lm0 $lr0\n");
        fprintf(fp, "nop\n");
        // v^2
        fprintf(fp, "fvmul $ln0 $ln0 $nowrite\n");
        // x^2 + v^2
        fprintf(fp, "fvadd $lr0 $mauf $nowrite\n");
        // 0.5 * (x^2 + v^2)
        fprintf(fp, "fvmul $ls6 $mauf $nowrite\n");
        
        // 結果出力
        // $lb のアドレスを 4 * k でずらす
        fprintf(fp, "l1bmm@0 $mauf $lb%d\n", k * 4);
        fprintf(fp, "\n");
    }

    // --- 3. 終了コード (1回だけ出力) ---
    fprintf(fp, "\n");
    fprintf(fp, "d getf $lm0n0c0b0m0p0 1\n");
    fprintf(fp, "d getf $ln0n0c0b0m0p0 1\n");
    fprintf(fp, "d getf $lr0n0c0b0m0p0 4\n");
    fprintf(fp, "d getf $ls0n0c0b0m0p0 4\n");
    
    // 出力バッファのサイズ指定 (4 * loop_count)
    fprintf(fp, "d getf $lb0n0c0b0 %d\n", 4 * loop_count);

    // ファイルを閉じる
    fclose(fp);
    printf("完了しました。\n");

    return 0;
}
