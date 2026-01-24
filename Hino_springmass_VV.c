#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // ファイルを開く
    FILE *fp = fopen("hino_debug.vsm", "w");
    if (fp == NULL) {
        perror("ファイルを開けませんでした");
        return 1;
    }

    // printf を fprintf(fp, ...) に置き換え
    fprintf(fp, "imm f\"0.01\" $nowrite\n"
                "lpassa $aluf $lm0v #h=0.1\n"
                "imm f\"0\" $lr0v #v0=0\n"
                "imm f\"1.0\" $ls0v #x0=1.0\n"
                "imm f\"0.005\" $nowrite\n"
                "lpassa $aluf $lm8v #hk/2m=0.1\n"
                "imm f\"0.99995\" $nowrite\n"
                "lpassa $aluf $lm16v #1-kh^2/2m=0.995\n"
                "imm f\"0.5\" $nowrite\n"
                "lpassa $aluf $lm32v\n"
                "imm f\"1\" $nowrite\n"
                "lpassa $aluf $ln0v\n"
                "nop\n"
                "nop\n");

    for(int k=1; k<=70; k++){
        for (int i = 1;i <=5; i++){
            fprintf(fp, "fvmul $lr0v $lm0v $lr8v\n"
                        "nop/2\n"
                        "fvfma $ls0v $lm16v $lr8v $ls8v #x(%d)\n"
                        "nop/2\n"
                        "nop/2\n"
                        "fvpassa $ls8v $lr16v\n"
                      "nop/2\n"
                      "fvadd $ls0v $lr16v $ls16v\n"
                        "nop/2\n"
                        "fvfma $ls16v -$lm8v $lr0v $lr8v #v(%d)\n"
                        "nop/2\n"
                        "nop/2\n"
                      "fvpassa $lr16v $ls8v\n"
                      "nop/2\n"
                        "fvmul $lr8v $lm0v $lr0v\n"
                        "nop/2\n"
                        "fvfma $ls8v $lm16v $lr0v $ls0v #x(%d)\n"
                        "nop/2\n"
                        "nop/2\n"
                      "fvpassa $ls0v $lr16v\n"
                      "nop/2\n"
                      "fvadd $ls8v $lr16v $ls16v\n"
                      "nop/2\n"
                      "fvfma $ls16v -$lm8v $lr8v $lr0v #v(%d)\n"
                      "nop/2\n"
                      "fvpassa $lr16v $ls0v\n"
                        "nop/2\n"
                        "nop/2\n"
                        ,2*i-1,2*i-1,2*i,2*i
                        );
        }
        fprintf(fp, "fvmul $ls0v $ls0v $ls20v\n"
                   "nop/2\n"
                   "fvmul $lr0v $lr0v $lr20v\n"
                   "nop/2\n"
                   "fvadd $ls20v $lr20v $ls20v\n"
                   "nop/2\n"
                   "fvmul $ls20v $lm32v $ls20v\n"
                   "nop/2\n"
                   "fvmul $ls20v $ln0v $ls20v #Etotal(%d)\n"
                   "nop/2\n"
                 "l1bmm@0 $ls20v $lb%d\n"
                   ,10*k,4*k);
    }

    fprintf(fp, "d getf $lb0n0c0b0 2804\n");
    fprintf(fp, "d getf $lr0n0c0b0m0p0 1\n"
               "d getf $ls0n0c0b0m0p0 1\n");

    // ファイルを閉じる
    fclose(fp);

    return 0;
}