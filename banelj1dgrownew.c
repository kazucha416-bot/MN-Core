#include <stdio.h>
#include <stdlib.h> // exit() のために使用

int main(void) {
    FILE *fp;
    // 出力先ファイルパス
    const char *filepath = "/home/kazuki/mncore/banelj1dnew.vsm";
    int loop_count = 1; // 繰り返す回数

    // ファイルを開く (書き込みモード)
    fp = fopen(filepath, "w");
    if (fp == NULL) {
        printf("エラー: ファイル %s を開けません。\n", filepath);
        exit(1);
    }

    printf("アセンブリコードを %s に書き出します...\n", filepath);

    // --- 1回だけ挿入する初期化コード (コメント付き) ---
    fprintf(fp, "d set $lm0n0c0b0m0p0 5 3fa666663fa666663a83126f3a83126f3f8000003f8000003f8000003f8000003f8000003f800000\n");
    fprintf(fp, "d set $ln0n0c0b0m0p0 1 0000000000000000\n");
    fprintf(fp, "\n");
    fprintf(fp, "imm f\"4.0\" $t\n");
    fprintf(fp, "fvmul $lm8 $lm8 $nowrite\n");
    fprintf(fp, "fvmul $mauf $lm8 $nowrite\n");
    fprintf(fp, "fvmul $mauf $mauf $lr0\n");
    fprintf(fp, "fvmul $t $lm6 $ls0\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "fvmul $lr0 $lr0 $lr2\n");
    fprintf(fp, "fvmul $ls0 $lr0 $lr0\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $ls0 $lr2 $lr2\n");
    fprintf(fp, "imm f\"6.0\" $nowrite\n");
    fprintf(fp, "fvmul $aluf $lr0 $ls0\n");
    fprintf(fp, "imm f\"12.0\" $nowrite\n");
    fprintf(fp, "fvmul $aluf $lr2 $ls2\n");
    fprintf(fp, "\n");
    fprintf(fp, "#最初の力を計算\n");
    fprintf(fp, "fvmul $lm0 $lm0 $lr4\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "frsqrt $lr4 $nowrite\n");
    fprintf(fp, "fvmul $aluf $aluf $ls4\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "imm f\"2.0\" $nowrite\n");
    fprintf(fp, "fvfma $lr4 -$ls4 $aluf $nowrite\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $ls4 $mauf $lr6 #r2iが求まった\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $lr6 $lr6 $ls6\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $lr6 $ls6 $lr8 #r06iが求まった\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $lr8 $lr8 $lr10 #r12iが求まった\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "fvmul $ls0 $lr8 $nowrite\n");
    fprintf(fp, "fvfma $ls2 $lr10 -$mauf $nowrite\n");
    fprintf(fp, "fvmul $mauf $lr6 $ls8 #fcが求まった\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $ls8 $lm0 $ls10 #f1が求まった\n");
    fprintf(fp, "\n");
    fprintf(fp, "#1/massの配列を作る\n");
    fprintf(fp, "frsqrt $lm4 $nowrite\n");
    fprintf(fp, "fvmul $aluf $aluf $ls4\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "imm f\"2.0\" $nowrite\n");
    fprintf(fp, "fvfma $lm4 -$ls4 $aluf $nowrite\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $ls4 $mauf $lm10  #1/massが求まった\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "fvmul $lm10 $ls10 $ls12  #f1/mass\n");
    fprintf(fp, "\n");
    fprintf(fp, "#dt*dt*0.5を作る\n");
    fprintf(fp, "fvmul $lm2 $lm2 $lr4\n");
    fprintf(fp, "imm f\"0.5\" $nowrite\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "fvmul $lr4 $aluf $lr12 #0.5*h*hが求まった\n");
    fprintf(fp, "\n");
    fprintf(fp, "#　pos + h*v　の計算\n");
    fprintf(fp, "fvpassa $lm2 $lr14\n");
    // --- 挿入ブロックここまで ---


    // --- ここからが100回繰り返すループ本体 (コメント・改行なし) ---
    for (int k = 0; k < loop_count; k++) {
        fprintf(fp, "fvpassa $ln0 $ls14\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "\n");
        fprintf(fp, "fvmul $lm10 $ls10 $ls12\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $lr14 $ls14 $lm0 $nowrite\n");
        fprintf(fp, "fvfma $lr12 $ls12 $mauf $lm0\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $lm0 $lm0 $lr4\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "frsqrt $lr4 $nowrite\n");
        fprintf(fp, "fvmul $aluf $aluf $ls4\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "imm f\"2.0\" $nowrite\n");
        fprintf(fp, "fvfma $lr4 -$ls4 $aluf $nowrite\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $ls4 $mauf $lr6\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $lr6 $lr6 $ls6\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $lr6 $ls6 $lr8\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $lr8 $lr8 $lr10\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvmul $ls0 $lr8 $nowrite\n");
        fprintf(fp, "fvfma $ls2 $lr10 -$mauf $nowrite\n");
        fprintf(fp, "fvmul $mauf $lr6 $ls16\n"); // fc
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $ls16 $lm0 $lr16\n"); // f2
        fprintf(fp, "imm f\"0.5\" $nowrite\n");
        fprintf(fp, "fvmul $aluf $lm2 $t\n");
        fprintf(fp, "fvadd $ls10 $lr16 $nowrite\n"); // f1 + f2
        fprintf(fp, "fvfma $mauf $t $ln0 $ln0\n"); // v update
        fprintf(fp, "fvpassa $lr16 $ls10\n"); // f1 = f2
        fprintf(fp, "fvpassa $lr8 $nowrite\n");
        fprintf(fp, "fvmul $mauf $lr0 $t\n");
        fprintf(fp, "fvpassa $lr10 $nowrite\n");
        fprintf(fp, "fvfma $lr2 $mauf -$t $lm12\n");
        fprintf(fp, "imm f\"0.5\" $nowrite\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvmul $aluf $lm4 $t\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $ln0 $ln0 $nowrite\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul $mauf $t $lm14\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvpassa $lm14 $nowrite\n");
        fprintf(fp, "fvadd $mauf $lm12 $nowrite\n");
        fprintf(fp, "fvpassa $mauf $lm16\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "l1bmm@0 $lm16v $lb%d\n", k * 4); // $lb0, $lb4, $lb8...
    }
    // --- ループここまで ---


    // --- ファイル末尾に挿入する終了コード ---
    fprintf(fp, "\n");
    fprintf(fp, "d getf $lm0n0c0b0m0p0 16\n");
    fprintf(fp, "d getf $ln0n0c0b0m0p0 16\n");
    fprintf(fp, "d getf $lr0n0c0b0m0p0 16\n");
    fprintf(fp, "d getf $ls0n0c0b0m0p0 16\n");
    fprintf(fp, "d getf $lb0n0c0b0 %d\n", 4 * loop_count);
    // --- 挿入ブロックここまで ---

    // ファイルを閉じる
    fclose(fp);
    printf("完了しました。\n");

    return 0;
}
