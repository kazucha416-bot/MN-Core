#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("baneVVnov.vsm", "w");
    if (fp == NULL) {
        perror("Failed to open baneVVnov.vsm for writing");
        return 1;
    }

    /* ヘッダ（1〜10行目） */
    fprintf(fp, "imm f\"0.01\" $lr0 #h=0.1\n");
    fprintf(fp, "imm f\"0.005\" $lr8 #h/2=0.05\n");
    fprintf(fp, "imm f\"1.0\" $lr16 #k/m=1.0\n");
    fprintf(fp, "imm f\"-1.0\" $ls0 #a_0=-1.0\n");
    fprintf(fp, "imm f\"0.0\" $nowrite\n");
    fprintf(fp, "lpassa $aluf $lm0 #v_0=0.0\n");
    fprintf(fp, "imm f\"1.0\" $nowrite\n");
    fprintf(fp, "lpassa $aluf $ln0 #x_0=1.0\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "nop\n\n");

    /* 11行目以降のブロックを 10 回繰り返す（x,a,v の番号を 1..10 に増やす） */
    for (int i = 1; i <= 700; i++) {
        fprintf(fp, "fvfma $ls0 $lr8 $lm0 $lm0\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $lm0 $lr0 $ln0 $ln0 #x(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvmul -$lr16 $ln0 $ls0 #a(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $ls0 $lr8 $lm0 $lm0 #v(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n\n");
    }
    fprintf(fp, "d getf $lm0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $ln0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $lr0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $ls0n0c0b0m0p0 12\n");

    fclose(fp);
    return 0;
}
