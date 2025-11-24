#include <stdio.h>
#include <stdint.h> // 32ビット整数 (uint32_t) のために必要

// 粒子数を32に設定
int num = 32; 

// 32-bit float と 32-bit 整数を同じメモリ領域で扱うための共用体
union Float32_Converter {
    float    f; // 32-bit float
    uint32_t u; // 32-bit unsigned integer
};

int main(void){

    // 1. 初期位置 (FCC格子) の生成
    // nx=2, ny=2, nz=2 に設定 (2*2*2=8セル, 8*4=32粒子)
    int a = 2, nx = 2, ny = 2, nz = 2, n = -1;
    float pos0[3][4] = {{0, 0, a/2.0, a/2.0},
                      {0, a/2.0, a/2.0, 0},
                      {0, a/2.0, 0, a/2.0}},
          pos[3][num]; // pos配列は [3][32] のサイズで確保される

    // 2x2x2 の三重ループ
    for(int jx=1; jx<=nx; jx++){
        for(int jy=1; jy<=ny; jy++){
            for(int jz=1; jz<=nz; jz++){
                n = n + 1;
                pos[0][n] = pos0[0][0] + (jx - 1) * a;
                pos[1][n] = pos0[1][0] + (jy - 1) * a;
                pos[2][n] = pos0[2][0] + (jz - 1) * a;
                n = n + 1;
                pos[0][n] = pos0[0][1] + (jx - 1) * a;
                pos[1][n] = pos0[1][1] + (jy - 1) * a;
                pos[2][n] = pos0[2][1] + (jz - 1) * a;
                n = n + 1;
                pos[0][n] = pos0[0][2] + (jx - 1) * a;
                pos[1][n] = pos0[1][2] + (jy - 1) * a;
                pos[2][n] = pos0[2][2] + (jz - 1) * a;
                n = n + 1;
                pos[0][n] = pos0[0][3] + (jx - 1) * a;
                pos[1][n] = pos0[1][3] + (jy - 1) * a;
                pos[2][n] = pos0[2][3] + (jz - 1) * a;
            }
        }
    }
    // この時点で n=31 となり、pos[3][32] がすべて埋まる

    // --- 2. 最終的な初期位置を8桁16進数で出力 ---
    
    printf("--- 初期位置 (32-bit / 8-digit Hex) ---\n");
    
    // 変換用の共用体を宣言
    union Float32_Converter converter;

    for (int i = 0; i < 3; i++) { // i = 0 (px), 1 (py), 2 (pz)
        if (i == 0) printf("px: ");
        if (i == 1) printf("py: ");
        if (i == 2) printf("pz: ");
        
        for (int j = 0; j < num; j++) { // j = 粒子インデックス (0~31)
            
            // 1. float値を共用体にセット
            converter.f = pos[i][j];
            
            // 2. 整数として解釈し、8桁の16進数(0埋め)で出力
            printf("%08x ", converter.u); 
        }
        printf("\n"); // 各行 (px, py, pz) の終わりで改行
    }
    printf("----------------------------------------\n");
    
    // (この後、シミュレーションのメインループが続く...)

    return 0;
}
