#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h> // 32ビット整数 (uint32_t) のために必要
#include <math.h>   // pow() と sqrt() のために必要

int num = 32;
int time_steps = 1000; // time()関数と名前が衝突するため変更

// 32-bit float と 32-bit 整数を同じメモリ領域で扱うための共用体
union Float32_Converter {
    float    f; // 32-bit float
    uint32_t u; // 32-bit unsigned integer
};

int main(void){
    /* 1. initial values & random velocity */
    float v[3][num], vmean[3];

    srand((unsigned int)time(NULL)); 

    for(int i=0; i<3; i++){
        vmean[i] = 0;
        for(int j=0; j<num; j++){
            v[i][j] = (rand() / (float)RAND_MAX) * 2.0 - 1.0;
            vmean[i] = vmean[i] + v[i][j];
        }
        vmean[i] = vmean[i] / num;
    }
    
    /* 2. 重心の移動をキャンセル */
    for(int j=0; j<num; j++){
        v[0][j] = v[0][j] - vmean[0];
        v[1][j] = v[1][j] - vmean[1];
        v[2][j] = v[2][j] - vmean[2];
    }

    /* 3. velocity scale (温度スケーリング) */
    float ke, temp, temp0 = 1.0;
    ke = 0.0;
    for(int j=0; j<num; j++){
        // 質量 m=1 として 0.5 * m * v^2 を計算
        ke +=  0.5 * (pow(v[0][j],2) + pow(v[1][j],2) + pow(v[2][j],2));
    }
    ke /= num; // 粒子1個あたりの平均運動エネルギー
    temp = ke / 1.5; // T = <KE> / (3/2 * kB), (kB=1)
    
    // スケーリング係数を計算
    float scale_factor = sqrt(temp0 / temp);

    // 全粒子の速度をスケーリング
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){
            v[i][j] *= scale_factor;
        }
    }

    // --- 4. 最終的な初期速度を8桁16進数で出力 ---
    
    printf("--- 最終的な初期速度 (32-bit / 8-digit Hex) ---\n");
    
    // 変換用の共用体を宣言
    union Float32_Converter converter;

    for (int i = 0; i < 3; i++) { // i = 0 (vx), 1 (vy), 2 (vz)
        if (i == 0) printf("vx: ");
        if (i == 1) printf("vy: ");
        if (i == 2) printf("vz: ");
        
        for (int j = 0; j < num; j++) { // j = 粒子インデックス
            
            // 1. 最終的な float値を共用体にセット
            converter.f = v[i][j];
            
            // 2. 整数として解釈し、8桁の16進数(0埋め)で出力
            printf("%08x ", converter.u); 
        }
        printf("\n"); // 各行 (vx, vy, vz) の終わりで改行
    }
    printf("----------------------------------------------\n");

    return 0;
}
