#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("banemasunew.vsm", "w");
    if (fp == NULL) {
        perror("ファイルを開けませんでした");
        return 1;
    }

    // 初期化部分
    fprintf(fp, "d set $lm0n0c0b0m0p0 10 3DCCCCCD000000000000000000000000000000000000000000000000000000003F800000000000000000000000000000000000000000000000000000000000003F000000000000000000000000000000\n");
    fprintf(fp, "imm f\"1.0\" $ls0v/1000 #x0=1.0\n");
    fprintf(fp, "imm f\"0\" $lr0v #v0=0\n");

    int lb_addr = 0; // $lb のアドレスを 0,2,4,... と増やすためのカウンタ

    // 繰り返し部分
    for (int i = 1; i <= 70; i++) {
        fprintf(fp, "fvmul -$lm8v $ls0v $ls256v\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $ls256v $lm0v $lr0v $lr0v #v(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $lr0v $lm0v $ls0v $ls0v #x(%d)\n", i);
        fprintf(fp, "nop\n");
         // 10ステップごとに指定のブロックを挿入
        if (i % 10 == 0) {
            fprintf(fp, "fvmul $lr0v $lr0v $lr64v\n");
            fprintf(fp, "fvmul $ls0v $ls0v $ls64v\n");
            fprintf(fp, "nop\n");
            fprintf(fp, "fvadd $lr64v $ls64v $ln0v\n");
            fprintf(fp, "nop/2\n");
            fprintf(fp, "fvmul $lm16v $ln0v $ln0v\n");
            fprintf(fp, "nop/2\n");
            fprintf(fp, "l1bmm@0 $ln0v $lb%d\n", lb_addr);
            lb_addr += 4; // 次回は4増やす
        }
    }

    fprintf(fp,"d getf $lm0n0c0b0m0p0 12\n");
    fprintf(fp,"d getf $ln0n0c0b0m0p0 1\n");
    fprintf(fp,"d getf $lr0n0c0b0m0p0 1\n");
    fprintf(fp,"d getf $ls0n0c0b0m0p0 1\n");
    fprintf(fp,"d getf $lb0n0c0b0 256\n");

    fclose(fp);
    return 0;
}
