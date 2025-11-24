#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp = fopen("banemasunew.vsm", "w");
    if (fp == NULL) {
        perror("ファイルを開けませんでした");
        return 1;
    }

    // ループ回数を変数として定義
    int max_loop = 7000;

    // 初期化部分
    fprintf(fp, "d set $lm0n0c0b0m0p0 10 3a83126f000000000000000000000000000000000000000000000000000000003F800000000000000000000000000000000000000000000000000000000000003F000000000000000000000000000000\n");
    fprintf(fp, "imm f\"1.0\" $ls0v/1000 #x0=1.0\n");
    fprintf(fp, "imm f\"0\" $lr0v #v0=0\n");

    int lb_addr = 0; // $lb のアドレスを 0,2,4,... と増やすためのカウンタ

    // 繰り返し部分 (max_loopを使用)
    for (int i = 1; i <= max_loop; i++) {
        fprintf(fp, "fvmul -$lm8v $ls0v $nowrite\n");
        fprintf(fp, "fvfma $mauf $lm0v $lr0v $lr0v #v(%d)\n", i);
        fprintf(fp, "nop\n");
        fprintf(fp, "fvfma $lr0v $lm0v $ls0v $ls0v #x(%d)\n", i);
        fprintf(fp, "nop\n");
        
        // 10ステップごとに指定のブロックを挿入
        if (i % 10 == 0) {
            fprintf(fp, "fvmul $lr0v $lr0v $lr64v\n");
            fprintf(fp, "fvmul $ls0v $ls0v $nowrite\n");
            fprintf(fp, "fvadd $lr64v $mauf $nowrite\n");
            fprintf(fp, "fvmul $lm16v $mauf $nowrite\n");
            fprintf(fp, "l1bmm@0 $mauf $lb%d\n", lb_addr);
            lb_addr += 4; // 次回は4増やす
        }
    }

    // 最後の出力サイズを計算: (ループ数 / 10) * 4
    // 例: (70 / 10) * 4 = 7 * 4 = 28
    int getf_size = (max_loop / 10) * 4;
   
    fprintf(fp, "d getf $lb0n0c0b0 %d\n", getf_size);
    fprintf(fp, "d getf $lm0n0c0b0m0p0 16\n");

    fclose(fp);
    return 0;
}

