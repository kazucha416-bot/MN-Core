#include <stdio.h>
#include <math.h> // powf(), sqrtf() を使う
#include <stdlib.h>

// --- グローバル設定 ---
const int time_steps = 2000;
const float dt = 0.001f;     // floatに変更
const float mass = 1.0f;     // floatに変更
const float eps = 1.0f;      // floatに変更
const float sigma = 1.0f;    // floatに変更

int main(void) {
    
    // --- 1. 変数とLJ係数の初期化 ---
    
    // 運動する粒子の状態 (1次元)
    float pos; // x座標
    float v;   // x速度
    float f1;  // 現在の力 (t)
    float f2;  // 次の力 (t+dt)
    
    // LJ係数の事前計算
    float ce12 = 4.0f * eps * powf(sigma, 12); // powf に変更
    float ce06 = 4.0f * eps * powf(sigma, 6);  // powf に変更
    float cf12 = ce12 * 12.0f;
    float cf06 = ce06 * 6.0f;

    // エネルギー計算用
    float r2, r2i, r06i, r12i, fc;
    float pe, ke, total_e;

    // --- 2. 粒子の初期条件 ---
    
    // 初期位置 (r = x)
    pos = 1.3f;
    
    // 初期速度 (静かに放す)
    v = 0.0f;

    // --- 3. 出力ファイルの準備 ---
    FILE *fp;
    fp = fopen("lj_oscillator_1D_float.txt", "w"); // ファイル名を変更
    if (fp == NULL) {
        printf("ファイルを開けません。\n");
        return 1;
    }
    fprintf(fp, "# Time\tPos\tPotentialE\tKineticE\tTotalE\n");

    // --- 4. 最初の力 (force1) を計算 ---
    r2 = pos * pos; // 1Dの距離の2乗
    r2i = 1.0f / r2;
    r06i = powf(r2i, 3); // powf に変更
    r12i = r06i * r06i;
    fc = (cf12 * r12i - cf06 * r06i) * r2i; // F(r)/r
    f1 = fc * pos; // Fx = (F(r)/r) * x

    // --- 5. 時間発展メインループ (ベレの速度形式) ---
    for (int k = 0; k < time_steps; k++) {
        
        // --- 5a. 位置の更新 (Verlet Step 1) ---
        pos = pos + dt * v + 0.5f * dt * dt * (f1 / mass);

        // --- 5b. 新しい位置での力 (force2) を計算 (Verlet Step 2) ---
        r2 = pos * pos; // 1Dの距離の2乗
        r2i = 1.0f / r2;
        r06i = powf(r2i, 3); // powf に変更
        r12i = r06i * r06i;
        fc = (cf12 * r12i - cf06 * r06i) * r2i;
        f2 = fc * pos;

        // --- 5c. 速度の更新 (Verlet Step 3) ---
        v = v + 0.5f * dt / mass * (f1 + f2);

        // --- 5d. 次のステップの準備 ---
        f1 = f2;

        // --- 5e. エネルギーの計算とファイルへの出力 ---
        pe = ce12 * r12i - ce06 * r06i; // ポテンシャルエネルギー
        ke = 0.5f * mass * (v * v);     // 1Dの運動エネルギー
        total_e = pe + ke;
        
        // fprintfの%fはfloat型もdouble型も扱えます
        fprintf(fp, "%f\t%f\t%f\t%f\t%f\n", (k * dt), pos, pe, ke, total_e);
    }

    // --- 6. クローズ処理 ---
    fclose(fp);
    printf("シミュレーション完了。 'lj_oscillator_1D_float.txt' に結果を出力しました。\n");

    return 0;
}
