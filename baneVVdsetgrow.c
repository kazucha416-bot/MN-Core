#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("baneVVdset.vsm", "w");
    if (fp == NULL) {
        perror("Failed to open baneVVdset.vsm for writing");
        return 1;
    }

    /* ヘッダ（1〜10行目） */
    fprintf(fp, "d set $lr0n0c0b0m0p0 1 3F847AE147AE147B #h=0.01\n");
    fprintf(fp, "d set $lr2n0c0b0m0p0 1 3F747AE147AE147B #h/2=0.005\n");
    fprintf(fp, "d set $lr4n0c0b0m0p0 1 3FF0000000000000 #k/m=1.0\n");
    fprintf(fp, "d set $ls0n0c0b0m0p0 1 BFF0000000000000 #a_0=-1.0\n");
    fprintf(fp, "d set $lm0n0c0b0m0p0 1 0000000000000000\n");
    fprintf(fp, "d set $ln0n0c0b0m0p0 1 3FF0000000000000#v_0=0.0\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "nop\n\n");

    /* 11行目以降のブロックを 10 回繰り返す（x,a,v の番号を 1..10 に増やす） */
    for (int i = 1; i <= 700; i++) {
        fprintf(fp, "fvfma $ls0 $lr2 $lm0 $lm0\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $lm0 $lr0 $ln0 $ln0 #x(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n");
         fprintf(fp, "fvmul -$lr4 $ln0 $ls0 #a(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $ls0 $lr8 $lm0 $lm0 #v(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "nop\n\n");
    }
    fprintf(fp, "d getf $lm0n0c0b0m0p0 6\n");
    fprintf(fp, "d getf $ln0n0c0b0m0p0 6\n");
    fprintf(fp, "d getf $lr0n0c0b0m0p0 6\n");
    fprintf(fp, "d getf $ls0n0c0b0m0p0 6\n");

    fclose(fp);
    return 0;
}
