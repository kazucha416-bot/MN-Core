#include <stdio.h>
#include <math.h> 
#include <stdlib.h>

// --- グローバル設定 ---
const int time_steps = 2000;
const double dt = 0.001;
const double mass = 1.0;
const double eps = 1.0;
const double sigma = 1.0;

// ★追加: クーロン相互作用の係数 (k * q1 * q2)
// 正の値なら斥力(反発)、負の値なら引力(引き合う)
// ここでは -10.0 にして「強い引力」を加えてみます（イオン結合のようなイメージ）
const double q_coeff = -10.0; 

int main(void) {
    
    // --- 1. 変数とLJ係数の初期化 ---
    
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
    double r, r2, r2i, r06i, r12i;
    double fc_lj, fc_coul, fc_total; // 力の係数 (Force/r)
    double pe_lj, pe_coul, pe_total, ke, total_e;

    // --- 2. 粒子の初期条件 ---
    pos = 1.3;
    v = 0.0;

    // --- 3. 出力ファイルの準備 ---
    FILE *fp;
    fp = fopen("lj_coulomb_1D.txt", "w"); // ファイル名変更
    if (fp == NULL) {
        printf("ファイルを開けません。\n");
        return 1;
    }
    // ヘッダーにクーロンエネルギーの列も追加しておくと解析しやすいかもですが、今回は合計で出します
    fprintf(fp, "# Time\tPos\tPotentialE\tKineticE\tTotalE\n");

    // --- 4. 最初の力 (force1) を計算 ---
    r2 = pos * pos;
    r = sqrt(r2);   // ★追加: クーロン力には r の1乗が必要なので平方根を取る
    r2i = 1.0 / r2;
    r06i = pow(r2i, 3);
    r12i = r06i * r06i;

    // LJの力 (F/r)
    fc_lj = (cf12 * r12i - cf06 * r06i) * r2i;
    
    // ★追加: クーロン力 (F = q/r^2) -> (F/r = q/r^3)
    // r^3 は (r^2 * r) で計算
    fc_coul = q_coeff / (r2 * r);

    // 合力係数
    fc_total = fc_lj + fc_coul;
    f1 = fc_total * pos;

    // --- 5. 時間発展メインループ ---
    for (int k = 0; k < time_steps; k++) {
         // --- 5e. エネルギーの計算と出力 ---
        
        // LJポテンシャル
        pe_lj = ce12 * r12i - ce06 * r06i;
        
        // ★追加: クーロンポテンシャル (V = q/r)
        pe_coul = q_coeff / r;
        
        pe_total = pe_lj + pe_coul;
        ke = 0.5 * mass * (v * v);
        total_e = pe_total + ke;
        
        fprintf(fp, "%f\t%f\t%f\t%f\t%f\n", (k * dt), pos, pe_total, ke, total_e);

        // --- 5a. 位置の更新 ---
        pos = pos + dt * v + 0.5 * dt * dt * (f1 / mass);

        // --- 5b. 新しい位置での力 (force2) を計算 ---
        r2 = pos * pos;
        r = sqrt(r2); // ★追加: 新しい r を計算
        r2i = 1.0 / r2;
        r06i = pow(r2i, 3);
        r12i = r06i * r06i;
        
        // 力の再計算
        fc_lj = (cf12 * r12i - cf06 * r06i) * r2i;
        fc_coul = q_coeff / (r2 * r); // ★追加: クーロン力
        
        fc_total = fc_lj + fc_coul;
        f2 = fc_total * pos;

        // --- 5c. 速度の更新 ---
        v = v + 0.5 * dt / mass * (f1 + f2);

        // --- 5d. 次のステップの準備 ---
        f1 = f2;
    }

    // --- 6. クローズ処理 ---
    fclose(fp);
    printf("シミュレーション完了。 'lj_coulomb_1D.txt' に結果を出力しました。\n");

    return 0;
}