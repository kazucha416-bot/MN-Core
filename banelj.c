#include <stdio.h>
#include <math.h> // pow(), sqrt() を使う
#include <stdlib.h> // (標準ライブラリ)

// --- グローバル設定 ---
const int time_steps = 2000; // ステップ数を2000に
const double dt = 0.001;     // 時間刻み幅 (ばねより振動が激しいため小さく設定)
const double mass = 1.0;     // 質量
const double eps = 1.0;      // LJパラメータ (ポテンシャルの深さ)
const double sigma = 1.0;    // LJパラメータ (距離)

int main(void) {
    
    // --- 1. 変数とLJ係数の初期化 ---
    
    // 運動する粒子の状態
    double pos_x, pos_y, pos_z;
    double v_x, v_y, v_z;
    double f1_x, f1_y, f1_z; // 現在の力 (t)
    double f2_x, f2_y, f2_z; // 次の力 (t+dt)
    
    // LJ係数の事前計算 (MDコードと同じ)
    double ce12 = 4.0 * eps * pow(sigma, 12);
    double ce06 = 4.0 * eps * pow(sigma, 6);
    double cf12 = ce12 * 12.0;
    double cf06 = ce06 * 6.0;

    // エネルギー計算用
    double r2, r2i, r06i, r12i, fc;
    double pe, ke, total_e;

    // --- 2. 粒子の初期条件 ---
    
    // 初期位置 (ポテンシャルが最小になる r ~ 1.12*sigma より少し離す)
    pos_x = 1.3;
    pos_y = 0.0;
    pos_z = 0.0;
    
    // 初期速度 (静かに放す)
    v_x = 0.0;
    v_y = 0.0;
    v_z = 0.0;

    // --- 3. 出力ファイルの準備 ---
    FILE *fp;
    fp = fopen("lj_oscillator.txt", "w");
    if (fp == NULL) {
        printf("ファイルを開けません。\n");
        return 1;
    }
    fprintf(fp, "# Time\tPosX\tPotentialE\tKineticE\tTotalE\n");

    // --- 4. 最初の力 (force1) を計算 ---
    r2 = pos_x*pos_x + pos_y*pos_y + pos_z*pos_z;
    r2i = 1.0 / r2;
    r06i = pow(r2i, 3);
    r12i = r06i * r06i;
    fc = (cf12 * r12i - cf06 * r06i) * r2i;
    f1_x = fc * pos_x;
    f1_y = fc * pos_y;
    f1_z = fc * pos_z;

    // --- 5. 時間発展メインループ (ベレの速度形式) ---
    for (int k = 0; k < time_steps; k++) {
        
        // --- 5a. 位置の更新 (Verlet Step 1) ---
        // x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
        pos_x = pos_x + dt * v_x + 0.5 * dt * dt * (f1_x / mass);
        pos_y = pos_y + dt * v_y + 0.5 * dt * dt * (f1_y / mass);
        pos_z = pos_z + dt * v_z + 0.5 * dt * dt * (f1_z / mass);

        // --- 5b. 新しい位置での力 (force2) を計算 (Verlet Step 2) ---
        // (★ ばね問題の F = -kx の部分が、このLJの力の計算に置き換わる ★)
        r2 = pos_x*pos_x + pos_y*pos_y + pos_z*pos_z;
        r2i = 1.0 / r2;
        r06i = pow(r2i, 3);
        r12i = r06i * r06i;
        fc = (cf12 * r12i - cf06 * r06i) * r2i;
        f2_x = fc * pos_x;
        f2_y = fc * pos_y;
        f2_z = fc * pos_z;

        // --- 5c. 速度の更新 (Verlet Step 3) ---
        // v(t+dt) = v(t) + 0.5 * (a(t) + a(t+dt)) * dt
        v_x = v_x + 0.5 * dt / mass * (f1_x + f2_x);
        v_y = v_y + 0.5 * dt / mass * (f1_y + f2_y);
        v_z = v_z + 0.5 * dt / mass * (f1_z + f2_z);

        // --- 5d. 次のステップの準備 ---
        f1_x = f2_x;
        f1_y = f2_y;
        f1_z = f2_z;

        // --- 5e. エネルギーの計算とファイルへの出力 ---
        pe = ce12 * r12i - ce06 * r06i; // ポテンシャルエネルギー
        ke = 0.5 * mass * (v_x*v_x + v_y*v_y + v_z*v_z); // 運動エネルギー
        total_e = pe + ke;
        
        fprintf(fp, "%f\t%f\t%f\t%f\t%f\n", (k * dt), pos_x, pe, ke, total_e);
    }

    // --- 6. クローズ処理 ---
    fclose(fp);
    printf("シミュレーション完了。 'lj_oscillator.txt' に結果を出力しました。\n");

    return 0;
}
