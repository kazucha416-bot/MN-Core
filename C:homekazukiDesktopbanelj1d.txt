#include <stdio.h>
#include <math.h> // pow(), sqrt() を使う
#include <stdlib.h>

// --- グローバル設定 ---
const int time_steps = 2000;
const double dt = 0.001;
const double mass = 1.0;
const double eps = 1.0;
const double sigma = 1.0;

int main(void) {
    
    // --- 1. 変数とLJ係数の初期化 ---
    
    // 運動する粒子の状態 (1次元)
    double pos; // x座標
    double v;   // x速度
    double f1;  // 現在の力 (t)
    double f2;  // 次の力 (t+dt)
    
    // LJ係数の事前計算
    double ce12 = 4.0 * eps * pow(sigma, 12);
    double ce06 = 4.0 * eps * pow(sigma, 6);
    double cf12 = ce12 * 12.0;
    double cf06 = ce06 * 6.0;

    // エネルギー計算用
    double r2, r2i, r06i, r12i, fc;
    double pe, ke, total_e;

    // --- 2. 粒子の初期条件 ---
    
    // 初期位置 (r = x)
    pos = 1.3;
    
    // 初期速度 (静かに放す)
    v = 0.0;

    // --- 3. 出力ファイルの準備 ---
    FILE *fp;
    fp = fopen("lj_oscillator_1D.txt", "w");
    if (fp == NULL) {
        printf("ファイルを開けません。\n");
        return 1;
    }
    fprintf(fp, "# Time\tPos\tPotentialE\tKineticE\tTotalE\n");

    // --- 4. 最初の力 (force1) を計算 ---
    r2 = pos * pos; // 1Dの距離の2乗
    r2i = 1.0 / r2;
    r06i = pow(r2i, 3);
    r12i = r06i * r06i;
    fc = (cf12 * r12i - cf06 * r06i) * r2i; // F(r)/r
    f1 = fc * pos; // Fx = (F(r)/r) * x

    // --- 5. 時間発展メインループ (ベレの速度形式) ---
    for (int k = 0; k < time_steps; k++) {
        
        // --- 5a. 位置の更新 (Verlet Step 1) ---
        pos = pos + dt * v + 0.5 * dt * dt * (f1 / mass);

        // --- 5b. 新しい位置での力 (force2) を計算 (Verlet Step 2) ---
        r2 = pos * pos; // 1Dの距離の2乗
        r2i = 1.0 / r2;
        r06i = pow(r2i, 3);
        r12i = r06i * r06i;
        fc = (cf12 * r12i - cf06 * r06i) * r2i;
        f2 = fc * pos;

        // --- 5c. 速度の更新 (Verlet Step 3) ---
        v = v + 0.5 * dt / mass * (f1 + f2);

        // --- 5d. 次のステップの準備 ---
        f1 = f2;

        // --- 5e. エネルギーの計算とファイルへの出力 ---
        pe = ce12 * r12i - ce06 * r06i; // ポテンシャルエネルギー
        ke = 0.5 * mass * (v * v);     // 1Dの運動エネルギー
        total_e = pe + ke;
        
        fprintf(fp, "%f\t%f\t%f\t%f\t%f\n", (k * dt), pos, pe, ke, total_e);
    }

    // --- 6. クローズ処理 ---
    fclose(fp);
    printf("シミュレーション完了。 'lj_oscillator_1D.txt' に結果を出力しました。\n");

    return 0;
}
