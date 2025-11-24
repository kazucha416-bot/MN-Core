#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>
#include <math.h>

#define NUM_PARTICLES 256
#define DIMENSIONS 3
#define TARGET_TEMP 1.0 // 設定温度 temp0

// 乱数の範囲 [-1.0, 1.0] を定義
#define RAND_RANGE 2.0
#define RAND_OFFSET 1.0

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

// --------------------------------------------------------
// 物理計算ロジック
// --------------------------------------------------------

double get_random_velocity() {
    return (rand() / (double)RAND_MAX) * RAND_RANGE - RAND_OFFSET;
}

void center_velocities(double v[DIMENSIONS][NUM_PARTICLES]) {
    double mean_v[DIMENSIONS] = {0.0, 0.0, 0.0};
    int i, d;

    for (d = 0; d < DIMENSIONS; d++) {
        for (i = 0; i < NUM_PARTICLES; i++) {
            mean_v[d] += v[d][i];
        }
        mean_v[d] /= NUM_PARTICLES;
    }

    for (d = 0; d < DIMENSIONS; d++) {
        for (i = 0; i < NUM_PARTICLES; i++) {
            v[d][i] -= mean_v[d];
        }
    }
}

double calculate_ke_and_temp(double v[DIMENSIONS][NUM_PARTICLES], double *ke) {
    double total_ke = 0.0;
    int i;

    for (i = 0; i < NUM_PARTICLES; i++) {
        double v_squared = 0.0;
        for (int d = 0; d < DIMENSIONS; d++) {
            v_squared += v[d][i] * v[d][i];
        }
        total_ke += 0.5 * v_squared;
    }
    
    *ke = total_ke / NUM_PARTICLES;
    return *ke / 1.5;
}

void scale_velocities(double v[DIMENSIONS][NUM_PARTICLES], double current_temp, double target_temp) {
    if (current_temp <= 1e-12) return;
    
    double scale_factor = sqrt(target_temp / current_temp);
    
    for (int d = 0; d < DIMENSIONS; d++) {
        for (int i = 0; i < NUM_PARTICLES; i++) {
            v[d][i] *= scale_factor;
        }
    }
}

// --------------------------------------------------------

int main() {
    double v[DIMENSIONS][NUM_PARTICLES];
    double current_ke, current_temp;
    int particle_idx;

    // 乱数シード
    srand((unsigned int)time(NULL));

    // 1. 初期速度生成
    for (int d = 0; d < DIMENSIONS; d++) {
        for (particle_idx = 0; particle_idx < NUM_PARTICLES; particle_idx++) {
            v[d][particle_idx] = get_random_velocity();
        }
    }

    // 2. 重心運動量の除去
    center_velocities(v);

    // 3. 初期温度計算
    current_temp = calculate_ke_and_temp(v, &current_ke);

    // 4. 温度スケーリング
    scale_velocities(v, current_temp, TARGET_TEMP);

    // 5. 指定フォーマットで出力
    // lrのベースアドレス: VX=$lr0, VY=$lr16, VZ=$lr32
    int lr_bases[3] = {0, 16, 32};
    
    // 次元ループ (0=VX, 1=VY, 2=VZ)
    for (int dim = 0; dim < 3; dim++) {
        
        // 64個ずつのブロックループ (計4ブロックで256個)
        // block 0: 0-63, block 1: 64-127, block 2: 128-191, block 3: 192-255
        for (int block = 0; block < 4; block++) {
            
            // ヘッダ出力: d seth $lr[base]n0c0b0m0p[block] 64
            printf("d seth $lr%dn0c0b0m0p%d 64 ", lr_bases[dim], block);
            
            // データ出力: ブロック内の64個の値をスペースなしで連続出力
            for (int i = 0; i < 64; i++) {
                int p_idx = block * 64 + i;
                // v[dim][p_idx] を半精度HEXで出力
                print_double_as_half_hex(v[dim][p_idx]);
            }
            
            // 1行終了
            printf("\n");
        }
    }

    return 0;
}
