#include <stdio.h>
#include <stdint.h>
#include <math.h>

// 粒子の数を定義
#define NUM_PARTICLES 256

// グリッドの次元
#define NX 4
#define NY 4
#define NZ 4

// 格子定数
#define A 2.0
#define HALF_A (A / 2.0)

// pos0に対応する初期オフセット座標 (4つの粒子位置)
const double pos0[3][4] = {
    {0.0, 0.0, HALF_A, HALF_A}, // xオフセット
    {0.0, HALF_A, HALF_A, 0.0}, // yオフセット
    {0.0, HALF_A, 0.0, HALF_A}  // zオフセット
};

// --- 浮動小数点数と16進数変換のための共用体と関数 ---

// 共用体を使ってdoubleのメモリ表現をunsigned long longとして読み出す
typedef union {
    double d;
    uint64_t u;
} double_converter;

/**
 * @brief double (64bit) の値を IEEE 754 half-precision (16bit) の
 * バイナリ表現に対応する4桁の16進数文字列で出力する。
 * 改行やスペースは含みません。
 * * @param val 変換するdouble値
 */
void print_double_as_half_hex(double val) {
    double_converter conv;
    conv.d = val;
    uint64_t d_bits = conv.u;
    
    // 64ビット形式の分解
    uint64_t d_sign = (d_bits >> 63) & 0x1;
    uint64_t d_exp = (d_bits >> 52) & 0x7FF;
    uint64_t d_mant = d_bits & 0xFFFFFFFFFFFFF;
    
    // 16ビット形式の構成要素
    uint16_t s_half; // 1ビット
    uint16_t e_half; // 5ビット
    uint16_t m_half; // 10ビット
    uint16_t h_bits; // 最終的な16ビット

    // 符号の変換
    s_half = (uint16_t)d_sign;

    // 指数の変換
    // Doubleの指数が0の場合はゼロとして扱う
    if (d_exp == 0) {
        e_half = 0;
        m_half = 0;
    } else {
        int exp_diff = (int)d_exp - 1023; // 実際の指数
        
        if (exp_diff > 15) { 
            // オーバーフロー -> 無限大 (Exponent: 31, Mantissa: 0)
            e_half = 31;
            m_half = 0;
        } else if (exp_diff < -14) {
            // アンダーフロー -> ゼロ (簡易化)
            e_half = 0;
            m_half = 0;
        } else {
            // 表現可能範囲内
            e_half = (uint16_t)(exp_diff + 15); // 新しいバイアス 15
            
            // 仮数の変換 (切り捨て)
            // 52ビットから10ビットに切り詰める (下位42ビットを破棄)
            m_half = (uint16_t)(d_mant >> 42); 
        }
    }

    // 16ビットに結合: [S (1bit)] [E (5bit)] [M (10bit)]
    h_bits = (s_half << 15) | (e_half << 10) | m_half;

    // 16ビットの整数を4桁の16進数として出力
    printf("%04X", h_bits); 
}

// --------------------------------------------------------

int main() {
    // 座標を格納する配列 (X, Y, Z × 256粒子)
    double pos[3][NUM_PARTICLES];
    int particle_idx = 0;

    // 1. 全粒子の座標を計算して配列に格納
    for (int jx = 0; jx < NX; jx++) {
        for (int jy = 0; jy < NY; jy++) {
            for (int jz = 0; jz < NZ; jz++) {
                for (int p = 0; p < 4; p++) {
                    if (particle_idx < NUM_PARTICLES) {
                        // 座標の計算 (double型)
                        pos[0][particle_idx] = pos0[0][p] + jx * A; // X
                        pos[1][particle_idx] = pos0[1][p] + jy * A; // Y
                        pos[2][particle_idx] = pos0[2][p] + jz * A; // Z
                        particle_idx++;
                    }
                }
            }
        }
    }

    if (particle_idx != NUM_PARTICLES) {
        fprintf(stderr, "エラー: 計算された粒子数 (%d) が期待値 (%d) と異なります。\n", particle_idx, NUM_PARTICLES);
        return 1;
    }

    // 2. 指定されたフォーマットで出力
    // lmのベースアドレス: X=$lm0, Y=$lm16, Z=$lm32
    int lm_bases[3] = {0, 16, 32};
    
    // 次元ループ (0=X, 1=Y, 2=Z)
    for (int dim = 0; dim < 3; dim++) {
        
        // 64個ずつのブロックループ (計4ブロックで256個)
        // block 0: 0-63, block 1: 64-127, block 2: 128-191, block 3: 192-255
        for (int block = 0; block < 4; block++) {
            
            // ヘッダ出力: d seth $lm[base]n0c0b0m0p[block] 64
            printf("d seth $lm%dn0c0b0m0p%d 64 ", lm_bases[dim], block);
            
            // データ出力: ブロック内の64個の値をスペースなしで連続出力
            for (int i = 0; i < 64; i++) {
                int p_idx = block * 64 + i;
                print_double_as_half_hex(pos[dim][p_idx]);
            }
            
            // 1行終了
            printf("\n");
        }
    }

    return 0;
}
