#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *fp;
    // 出力先ファイルパス (倍精度版なのでファイル名を変えています)
    const char *filepath = "/home/kazuki/mncore/baneljdouble.vsm";
    int loop_count = 2000; // 繰り返す回数

    // ファイルを開く (書き込みモード)
    fp = fopen(filepath, "w");
    if (fp == NULL) {
        printf("エラー: ファイル %s を開けません。\n", filepath);
        exit(1);
    }

    printf("倍精度アセンブリコードを %s に書き出します...\n", filepath);

    // --- 1. 初期化ブロック (1回だけ出力) ---
    fprintf(fp, "d set $lm0n0c0b0m0p0 5 3ff4cccccccccccd3f50624dd2f1a9fc3ff00000000000003ff00000000000003ff0000000000000\n");
    fprintf(fp, "d set $ln0n0c0b0m0p0 2 00000000000000003eb0c6f7a0b5ed8d\n");
    fprintf(fp, "d set $ls18n0c0b0m0p0 1 3fe0000000000000\n");
    fprintf(fp, "d set $lr20n0c0b0m0p0 1 4010000000000000\n");
    fprintf(fp, "dvmulu $lm8 $lm8 $nowrite\n");
    fprintf(fp, "dvmulu $mauf $lm8 $nowrite\n");
    fprintf(fp, "dvmulu $mauf $mauf $lr0\n");
    fprintf(fp, "dvmulu $lr20 $lm6 $ls0\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "dvmulu $lr0 $lr0 $lr2\n");
    fprintf(fp, "dvmulu $ls0 $lr0 $lr0\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $ls0 $lr2 $lr2\n");
    fprintf(fp, "immu i\"0x40180000\" $nowrite\n");
    fprintf(fp, "dvmulu $aluf $lr0 $ls0\n");
    fprintf(fp, "immu i\"0x40280000\" $nowrite\n");
    fprintf(fp, "dvmulu $aluf $lr2 $ls2\n");
    fprintf(fp, "\n");
    fprintf(fp, "dvmulu $lm0 $lm0 $lr4\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "drsqrt $lr4 $nowrite\n");
    fprintf(fp, "dvmulu $aluf $aluf $ls4\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "immu i\"0x40000000\" $nowrite\n");
    fprintf(fp, "dvfmau $lr4 -$ls4 $aluf $nowrite\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $ls4 $mauf $lr6 $ls4\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "immu i\"0x40000000\" $nowrite\n");
    fprintf(fp, "dvfmau $lr4 -$ls4 $aluf $nowrite\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $ls4 $mauf $lr6 $ls4\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $lr6 $lr6 $ls6\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $lr6 $ls6 $lr8\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $lr8 $lr8 $lr10\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "dvmulu $ls0 $lr8 $nowrite\n");
    fprintf(fp, "dvfmau $ls2 $lr10 -$mauf $nowrite\n");
    fprintf(fp, "dvmulu $mauf $lr6 $ls8\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $ls8 $lm0 $ls10\n");
    fprintf(fp, "\n");
    fprintf(fp, "drsqrt $lm4 $nowrite\n");
    fprintf(fp, "dvmulu $aluf $aluf $ls4\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "immu i\"0x40000000\" $nowrite\n");
    fprintf(fp, "dvfmau $lm4 -$ls4 $aluf $nowrite\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $ls4 $mauf $lm10 $ls4\n");
    fprintf(fp, "nop\n");
    fprintf(fp, "immu i\"0x40000000\" $nowrite\n");
    fprintf(fp, "dvfmau $lm4 -$ls4 $aluf $nowrite\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $ls4 $mauf $lm10 $ls4\n");
    fprintf(fp, "nop/2\n");
    fprintf(fp, "dvmulu $lm10 $ls10 $ls12\n");
    fprintf(fp, "\n");
    fprintf(fp, "dvmulu $ln2 $ls18 $lr12\n");
    fprintf(fp, "\n");
    fprintf(fp, "dvpassa $lm2 $lr14\n");
    fprintf(fp, "#ここからループ開始\n");
    
    // --- 2. ループ部分 (loop_count回) ---
    for (int k = 0; k < loop_count; k++) {
        fprintf(fp, "dvpassa $ln0 $ls14\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "\n");
        fprintf(fp, "dvfmau $lr14 $ls14 $lm0 $nowrite\n");
        fprintf(fp, "dvfmau $lr12 $ls12 $mauf $lm0\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $lm0 $lm0 $lr4\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "drsqrt $lr4 $nowrite\n");
        fprintf(fp, "dvmulu $aluf $aluf $ls4\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "immu i\"0x40000000\" $nowrite\n");
        fprintf(fp, "dvfmau $lr4 -$ls4 $aluf $nowrite\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $ls4 $mauf $lr6 $ls4\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "immu i\"0x40000000\" $nowrite\n");
        fprintf(fp, "dvfmau $lr4 -$ls4 $aluf $nowrite\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $ls4 $mauf $lr6 $ls4\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "\n");
        fprintf(fp, "dvmulu $lr6 $lr6 $ls6\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $lr6 $ls6 $lr8\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $lr8 $lr8 $lr10\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "dvmulu $ls0 $lr8 $nowrite\n");
        fprintf(fp, "dvfmau $ls2 $lr10 -$mauf $nowrite\n");
        fprintf(fp, "dvmulu $mauf $lr6 $ls16\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $ls16 $lm0 $lr16\n");
        fprintf(fp, "dvmulu $ls18 $lm2 $lr20\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "dvadd $ls10 $lr16 $nowrite\n");
        fprintf(fp, "dvfmau $mauf $lr20 $ln0 $ln0\n");
        fprintf(fp, "dvpassa $lr16 $ls10\n");
        fprintf(fp, "dvpassa $lr8 $nowrite\n");
        fprintf(fp, "dvmulu $mauf $lr0 $ls20\n");
        fprintf(fp, "dvpassa $lr10 $nowrite\n");
        fprintf(fp, "nop\n");
        fprintf(fp, "dvfmau $lr2 $mauf -$ls20 $lm12\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $ls18 $lm4 $lr20\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $ln0 $ln0 $nowrite\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvmulu $mauf $lr20 $lm14\n");
        fprintf(fp, "nop/2\n");
        fprintf(fp, "dvpassa $lm14 $nowrite\n");
        fprintf(fp, "dvadd $mauf $lm12 $nowrite\n");
        
        // ★ここが重要: 倍精度なのでアドレスは 8 ずつ増やす
        fprintf(fp, "l1bmm@0 $mauf $lb%d\n", k * 4); 
        
        fprintf(fp, "\n");
    }

    // --- 3. 終了ブロック (1回だけ出力) ---
    fprintf(fp, "\n");
    fprintf(fp, "d getd $lm0n0c0b0m0p0 20\n");
    fprintf(fp, "d getd $ln0n0c0b0m0p0 2\n");
    fprintf(fp, "d getd $lr0n0c0b0m0p0 20\n");
    fprintf(fp, "d getd $ls0n0c0b0m0p0 20\n");
    
    // ★ここも重要: データの総サイズは 8バイト * ループ回数
    fprintf(fp, "d getd $lb0n0c0b0 %d\n", 4 * loop_count);

    // ファイルを閉じる
    fclose(fp);
    printf("完了しました。\n");

    return 0;
}
