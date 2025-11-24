#include <stdio.h>
#include <math.h> // cos関数を使うために追加

// 加速度を計算する関数 a = -(k/m)x
// 繰り返し使うので関数にすると便利
double acceleration(double x, double k, double m) {
    return -(k / m) * x;
}

int main() {
    // パラメータの設定 (倍精度)
    const double h = 0.1;   // 時間の刻み幅 (time step)
    const double k = 1.0;   // ばね定数 (spring constant)
    const double m = 1.0;   // 質量 (mass)

    // 初期条件
    double x = 1.0;   // 初期位置 (initial position, x_0)
    double v = 0.0;   // 初期速度 (initial velocity, v_0)
    double t = 0.0;   // 初期時刻 (initial time)

    // 計算するステップ数
    const int num_steps = 10;

    // ヘッダー（見出し）の表示
    printf("ステップ\t 時刻 t\t\t 位置 x (RK4)\t\t 速度 v (RK4)\n");
    printf("------------------------------------------------------------------\n");

    // 初期状態の表示
    printf("%d\t\t %.2f\t\t %.8f\t %.8f\n", 0, t, x, v);

    // 時間を進めながら10ステップ分計算 (4次のルンゲ＝クッタ法)
    for (int i = 1; i <= num_steps; i++) {
        // --- 4次のルンゲ＝クッタ法の計算 ---

        // k1: 現在地の傾き
        double k1_v = acceleration(x, k, m);
        double k1_x = v;

        // k2: ステップの中間点(1)の傾き
        double k2_v = acceleration(x + k1_x * h / 2.0, k, m);
        double k2_x = v + k1_v * h / 2.0;

        // k3: ステップの中間点(2)の傾き (k2の値を使う)
        double k3_v = acceleration(x + k2_x * h / 2.0, k, m);
        double k3_x = v + k2_v * h / 2.0;

        // k4: ステップの終点の傾き
        double k4_v = acceleration(x + k3_x * h, k, m);
        double k4_x = v + k3_v * h;

        // 4つの傾きを重み付けして平均し、位置xと速度vを更新
        x = x + (h / 6.0) * (k1_x + 2.0 * k2_x + 2.0 * k3_x + k4_x);
        v = v + (h / 6.0) * (k1_v + 2.0 * k2_v + 2.0 * k3_v + k4_v);

        // 時刻 t を更新
        t = t + h;

        // 計算結果を表示
        printf("%d\t\t %.2f\t\t %.8f\t %.8f\n", i, t, x, v);
    }

    printf("\n--- 最終結果の比較 (t=1.0) ---\n");
    printf("4次ルンゲクッタ法: x = %.8f\n", x);
    printf("厳密解 (cos(1.0)): x = %.8f\n", cos(1.0));

    return 0;
}
