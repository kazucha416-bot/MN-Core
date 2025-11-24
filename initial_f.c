#include <stdio.h>
#include <math.h> 
#include <stdlib.h>
#include <stdint.h>

#define NUM 256     // 粒子の数
#define DIMENSIONS 3 // 3次元

// レナード・ジョーンズポテンシャル定数
#define EPSILON 1.0 
#define SIGMA 1.0   

// グリッドの次元 (pos生成用)
#define NX 4
#define NY 4
#define NZ 4
#define A 2.0
#define HALF_A (A / 2.0)

// pos0に対応する初期オフセット座標 (4つの粒子位置)
const double pos0[3][4] = {
    {0.0, 0.0, HALF_A, HALF_A}, // xオフセット
    {0.0, HALF_A, HALF_A, 0.0}, // yオフセット
    {0.0, HALF_A, 0.0, HALF_A}  // zオフセット
};

// 定数
const double CE12 = 4.0 * EPSILON * 1.0;
const double CE06 = 4.0 * EPSILON * 1.0;
const double CF12 = CE12 * 12.0;
const double CF06 = CE06 * 6.0;

// --- 浮動小数点数変換のための共用体と関数 ---

typedef union {
    double d;
    uint64_t u;
} double_converter;

/**
 * @brief double (64bit) の値を IEEE 754 half-precision (16bit) に変換し
 * 4桁の16進数文字列で出力する関数。改行やスペースは含みません。
 */
void print_double_as_half_hex(double val) {
    double_converter conv;
    conv.d = val;
    uint64_t d_bits = conv.u;

    // --- 64ビット(Double)の分解 ---
    uint64_t sign = (d_bits >> 63) & 0x1;
    uint64_t exp_double = (d_bits >> 52) & 0x7FF;
    uint64_t mant_double = d_bits & 0xFFFFFFFFFFFFF;

    // --- 16ビット(Half)の構築要素 ---
    uint16_t h_sign = (uint16_t)sign;
    uint16_t h_exp = 0;
    uint16_t h_mant = 0;

    // 指数の変換 (バイアス調整: 1023 -> 15)
    if (exp_double == 0) {
        h_exp = 0;
        h_mant = 0;
    } else {
        int exp_unbiased = (int)exp_double - 1023;
        int exp_half = exp_unbiased + 15;

        if (exp_half >= 31) {
            // オーバーフロー
            h_exp = 31;
            h_mant = 0;
        } else if (exp_half <= 0) {
            // アンダーフロー
            h_exp = 0;
            h_mant = 0;
        } else {
            // 通常の数値
            h_exp = (uint16_t)exp_half;
            // 仮数の変換: 上位10ビットを取得
            h_mant = (uint16_t)(mant_double >> 42);
        }
    }

    // 16ビットパターンの結合
    uint16_t half_bits = (h_sign << 15) | (h_exp << 10) | h_mant;

    // 4桁の16進数（大文字）で出力
    printf("%04X", half_bits);
}

// --- レナード-ジョーンズ相互作用計算関数 ---
void calculate_lj_forces_and_energy(double pos[DIMENSIONS][NUM], 
                                    double force1[DIMENSIONS][NUM], 
                                    double *engp) {
    
    double x, y, z;
    double r2, r2i, r06i, r12i;
    double ep;
    double fc;
    double fx, fy, fz;
    int i, j;
    
    // 初期化
    *engp = 0.0;
    for (i = 0; i < NUM; i++) {
        force1[0][i] = 0.0;
        force1[1][i] = 0.0;
        force1[2][i] = 0.0;
    }

    // 二体間相互作用の計算ループ
    for (j = 1; j < NUM; j++) { 
        for (i = 0; i < j; i++) { 
            
            x = pos[0][i] - pos[0][j];
            y = pos[1][i] - pos[1][j];
            z = pos[2][i] - pos[2][j];
            
            r2 = x*x + y*y + z*z;
            
            if (r2 < 1e-12) continue;
            
            r2i = 1.0 / r2;
            r06i = r2i * r2i * r2i;
            r12i = r06i * r06i;
            
            ep = CE12 * r12i - CE06 * r06i;
            *engp += ep;
            
            fc = (CF12 * r12i - CF06 * r06i) * r2i;
            
            fx = fc * x;
            fy = fc * y;
            fz = fc * z;

            force1[0][i] += fx;
            force1[1][i] += fy;
            force1[2][i] += fz;
            
            force1[0][j] -= fx;
            force1[1][j] -= fy;
            force1[2][j] -= fz;
        }
    }
}
// --------------------------------------------------------

int main() {
    // 1. 粒子の位置pos[3][256]の計算
    double pos[DIMENSIONS][NUM];
    int n = 0; 
    
    for (int jx = 0; jx < NX; jx++) {
        for (int jy = 0; jy < NY; jy++) {
            for (int jz = 0; jz < NZ; jz++) {
                for (int p = 0; p < 4; p++) {
                    if (n < NUM) {
                        pos[0][n] = pos0[0][p] + jx * A;
                        pos[1][n] = pos0[1][p] + jy * A;
                        pos[2][n] = pos0[2][p] + jz * A;
                        n++; 
                    }
                }
            }
        }
    }

    double force1[DIMENSIONS][NUM];
    double engp_result = 0.0;

    // 2. レナード-ジョーンズ相互作用の計算実行
    calculate_lj_forces_and_energy(pos, force1, &engp_result);

    // 3. 指定フォーマットで出力
    // lsのベースアドレス: FX=$ls0, FY=$ls16, FZ=$ls32
    int ls_bases[3] = {0, 16, 32};
    
    // 次元ループ (0=FX, 1=FY, 2=FZ)
    for (int dim = 0; dim < 3; dim++) {
        
        // 64個ずつのブロックループ (計4ブロックで256個)
        // block 0: 0-63, block 1: 64-127, block 2: 128-191, block 3: 192-255
        for (int block = 0; block < 4; block++) {
            
            // ヘッダ出力: d seth $ls[base]n0c0b0m0p[block] 64
            printf("d seth $ls%dn0c0b0m0p%d 64 ", ls_bases[dim], block);
            
            // データ出力: ブロック内の64個の値をスペースなしで連続出力
            for (int i = 0; i < 64; i++) {
                int p_idx = block * 64 + i;
                // force1[dim][p_idx] を半精度HEXで出力
                print_double_as_half_hex(force1[dim][p_idx]);
            }
            
            // 1行終了
            printf("\n");
        }
    }

    return 0;
}
