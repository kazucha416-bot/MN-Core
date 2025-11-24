#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("baneVVnew.vsm", "w");
    if (fp == NULL) {
        perror("Failed to open baneVVnew.vsm for writing");
        return 1;
    }

    /* ヘッダ（1〜10行目） */
    fprintf(fp, "imm f\"-1.0\" $ls0v #a0=-1.0\n");
    fprintf(fp, "d set $lm0n0c0b0m0p0 1 0000000000000000 #v0\n");
    fprintf(fp, "d set $ln0n0c0b0m0p0 4 3F8000003F8000003F8000003F8000003F8000003F8000003F8000003F800000 #x0n\n");
    fprintf(fp, "imm f\"0.1\" $lr0v #h=0.01\n");
    fprintf(fp, "imm f\"0.05\" $lr8v #h/2=0.005\n");
    fprintf(fp, "imm f\"1.0\" $lr16v #k/m=1.0\n");
    fprintf(fp, "imm f\"0.5\" $ls8v #エネルギーのための0.5\n");

    /* 11行目以降のブロックを 10 回繰り返す（x,a,v の番号を 1..10 に増やす） */
    for (int i = 1; i <= 70; i++) {
        fprintf(fp, "fvfma $ls0v $lr8v $lm0v $t #a0*h/2+v0=v0.5\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $t $lr0v $ln0v $ln0v #x(%d) v0.5*h+x0=x1\n", i);
        fprintf(fp, "nop/2\n");
        fprintf(fp, "fvmul -$lr16v $ln0v $ls0v #a(%d) -k/m*x1=a\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $ls0v $lr8v $t $lm0v #v(%d) a1*h/2+v0.5=v1\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "fvmul $ln0v $ln0v $lr24v\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "fvmul $lm0v $lm0v $nowrite\n");
        fprintf(fp, "fvadd $lr24v $mauf $nowrite\n");
        fprintf(fp, "fvmul $mauf $ls8v $nowrite\n");
        fprintf(fp, "l1bmm@0 $mauf $lb%d\n",i*4);
    }
    fprintf(fp, "d getf $lm0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $ln0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $lr0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $ls0n0c0b0m0p0 12\n");
    fprintf(fp, "d getf $tn0c0b0m0p0 12\n");
    fprintf(fp, "d getf $lb0n0c0b0 280\n");

    fclose(fp);
    return 0;
}


