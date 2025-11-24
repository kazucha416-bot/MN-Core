#include <stdio.h>

int main(void)
{
    printf("imm f\"0.1\" $nowrite\n"
           "lpassa $aluf $lm0v #h=0.1\n"
           "imm f\"0\" $lr0v #v0=0\n"
           "imm f\"1.0\" $ls0v #x0=1.0\n"
           "imm f\"0.9950041\" $nowrite\n"
           "lpassa $aluf $lm8v #1-kh2/2m+k2h4/24m2=0.9950041\n"
           "imm f\"0.09983333\" $nowrite\n"
           "lpassa $aluf $lm16v #1-kh3/6m=0.09983333\n"
		   "imm f\"0.09983333\" $nowrite\n"
           "lpassa $aluf $lm24v #-(-kh/m+k^2h^3/6m^2)=0.09983333\n"
           "nop\n"
           "nop\n");

    int i;
    for (i = 1; i <= 500; i++) {
        printf("fvmul $ls0v $lm8v $ls8v\n"
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
    }

    printf("d getf $lr0n0c0b0m0p0 4\n"
           "d getf $ls0n0c0b0m0p0 4\n");

    return 0;
}
