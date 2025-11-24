#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp;
    const char *filepath = "baneRK4.vsm";
    int loop_count = 70; // ループ回数 70

    fp = fopen(filepath, "w");
    if (fp == NULL) {
        printf("エラー: ファイル %s を開けません。\n", filepath);
        exit(1);
    }

    printf("アセンブリコードを %s に書き出します...\n", filepath);

    // --- 初期化部分 ---
    fprintf(fp, "imm f\"0.1\" $nowrite\n"
                "lpassa $aluf $lm0v #h=0.1\n"
                "imm f\"0\" $lr0v #v0=0\n"
                "imm f\"1.0\" $ls0v #x0=1.0\n"
                "imm f\"0.5\" $lr256v #Constant 0.5 for Energy Calc\n" // ★追加: エネルギー計算用の0.5
                "imm f\"0.9950041\" $nowrite\n"
                "lpassa $aluf $lm8v #1-kh2/2m+k2h4/24m2=0.9950041\n"
                "imm f\"0.09983333\" $nowrite\n"
                "lpassa $aluf $lm16v #1-kh3/6m=0.09983333\n"
                "imm f\"0.09983333\" $nowrite\n"
                "lpassa $aluf $lm24v #-(-kh/m+k^2h^3/6m^2)=0.09983333\n"
                "nop\n"
                "nop\n");

    // --- ループ部分 ---
    for (int i = 1; i <= loop_count; i++) {
        // 1. RK4の計算ステップ
        fprintf(fp, "fvmul $ls0v $lm8v $ls8v\n"
                    "nop\n"
                    "fvmul $lr0v $lm16v $lr8v\n"
                    "nop\n"
                    "fvadd $ls8v $lr8v $ls8v #x(%d)\n"
                    "nop\n"
                    "fvmul $lr0v $lm8v $lr0v\n"
                    "nop\n"
                    "fvmul $ls0v -$lm24v $ls0v\n"
                    "nop\n"
                    "fvadd $lr0v $ls0v $lr8v #v(%d)\n"
                    "nop\n"
                    "fvmul $ls8v $lm8v $ls0v\n"
                    "nop\n"
                    "fvmul $lr8v $lm16v $lr0v\n"
                    "nop\n"
                    "fvadd $ls0v $lr0v $ls0v #x(%d)\n"
                    "nop\n"
                    "fvmul $lr8v $lm8v $lr8v\n"
                    "nop\n"
                    "fvmul $ls8v -$lm24v $ls8v\n"
                    "nop\n"
                    "fvadd $lr8v $ls8v $lr0v #v(%d)\n"
                    "nop\n",
                    2 * i - 1, 2 * i - 1, 2 * i, 2 * i);

        // 2. ★追加: エネルギー計算とL1BM転送
        // Total E = 0.5 * (v^2 + x^2)
        fprintf(fp, "fvmul $lr0v $lr0v $t\n");        // v^2 -> $t
        fprintf(fp, "fvmul $ls0v $ls0v $nowrite\n");  // x^2 -> mauf
        fprintf(fp, "fvadd $mauf $t $nowrite\n");     // x^2 + v^2 -> mauf
        fprintf(fp, "fvmul $mauf $lr256v $nowrite\n");// * 0.5 -> mauf
        // アドレスを 0, 4, 8... と増やす (iは1始まりなので (i-1)*4)
        fprintf(fp, "l1bmm@0 $mauf $lb%d\n", (i - 1) * 4);
        fprintf(fp, "\n");
    }

    // --- 終了コード ---
    fprintf(fp, "d getf $lr0n0c0b0m0p0 4\n"
                "d getf $ls0n0c0b0m0p0 4\n");
    
    // ★追加: L1BMデータの取得
    fprintf(fp, "d getf $lb0n0c0b0 300\n");

    fclose(fp);
    printf("完了しました。\n");

    return 0;
}
