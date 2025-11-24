#include <stdio.h>

int main(void)
{
    FILE *fp = fopen("banemasu.vsm", "w");
    if (fp == NULL) {
        perror("ファイルを開けませんでした");
        return 1;
    }

    fprintf(fp, "imm f\"0.1\" $nowrite\n"
                "lpassa $aluf $lm0v #h=0.1\n"
                "imm f\"0\" $lr0v #v0=0\n"
                "imm f\"1.0\" $ls0v #x0=1.0\n"
                "imm f\"0.1\" $nowrite\n"
                "lpassa $aluf $lm8v #hk/m=0.1\n"
                "nop\n"
                "nop\n");
    int i;
    for (i = 1; i <= 500; i++) {
        fprintf(fp, "fvfma $lr0v $lm0v $ls0v $ls8v #x(%d)\n"
                    "nop\n"
                    "fvfma $ls0v -$lm8v $lr0v $lr0v #v(%d)\n"
                    "nop\n"
                    "nop\n"
                    "fvfma $lr0v $lm0v $ls8v $ls0v #x(%d)\n"
                    "nop\n"
                    "fvfma $ls8v -$lm8v $lr0v $lr0v #v(%d)\n"
                    "nop\n"
                    "nop\n"
                    , 2*i-1, 2*i-1, 2*i, 2*i
        );
    }
    fprintf(fp, "d getf $lr0n0c0b0m0p0 4\n"
                "d getf $ls0n0c0b0m0p0 4\n");

    fclose(fp);
    return 0;
}
