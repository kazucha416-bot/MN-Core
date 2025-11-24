#include <stdio.h>

int main() {
    // パラメータの設定
    const double h = 0.1;   // 時間の刻み幅 (time step)
    const double k = 1.0;   // ばね定数 (spring constant)
    const double m = 1.0;   // 質量 (mass)

    // 初期条件
    double x = 1.0;   // 初期位置 (initial position, x_0)
    double v = 0.0;   // 初期速度 (initial velocity, v_0)
    double t = 0.0;   // 初期時刻 (initial time)

    // 計算するステップ数
    const int num_steps = 70;

    // ヘッダー（見出し）の表示
    printf("ステップ\t 時刻 t\t\t 位置 x\t\t 速度 v\n");
    printf("----------------------------------------------------------\n");

    // 初期状態の表示
    printf("%d\t\t %.2f\t\t %.6f\t %.6f\n", 0, t, x, v);

    // 初期エネルギー表示（step 0）
    double KE = 0.5 * m * v * v;
    double PE = 0.5 * k * x * x;
    double E  = KE + PE;
    printf("\n[Energy] Step %d, t=%.2f -> KE=%.6f, PE=%.6f, Total=%.6f\n\n", 0, t, KE, PE, E);

    // 時間を進めながら計算
    for (int i = 1; i <= num_steps; i++) {
        // 1. 加速度 a を計算
        double a = -(k / m) * x;

        // 2. 速度 v を更新
        v = v + a * h;

        // 3. 位置 x を更新
        x = x + v * h;

        // 4. 時刻 t を更新
        t = t + h;

        // 5. 計算結果を表示（元の出力）
        printf("%d\t\t %.2f\t\t %.6f\t %.6f\n", i, t, x, v);

        // 6. 10ステップごとにエネルギーを出力
        if (i % 10 == 0) {
            KE = 0.5 * m * v * v;
            PE = 0.5 * k * x * x;
            E  = KE + PE;
            printf("\n[Energy] Step %d, t=%.2f -> KE=%.6f, PE=%.6f, Total=%.6f\n\n", i, t, KE, PE, E);
        }
    }

    return 0;
}
