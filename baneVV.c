#include <stdio.h>
#include <math.h> // cos関数を使うために追加

int main() {
    // パラメータの設定 (倍精度)
    const double h = 0.01;   // 時間の刻み幅 (time step)
    const double k = 1.0;   // ばね定数 (spring constant)
    const double m = 1.0;   // 質量 (mass)

    // 初期条件
    double x = 1.0;   // 初期位置 (initial position, x_0)
    double v = 0.0;   // 初期速度 (initial velocity, v_0)
    double t = 0.0;   // 初期時刻 (initial time)
    double a = -(k / m) * x; // 初期の加速度

    // 計算するステップ数
    const int num_steps = 200;

    // ヘッダー（見出し）の表示
    printf("ステップ\t 時刻 t\t\t 位置 x (V-Verlet)\t 速度 v (V-Verlet)\n");
    printf("--------------------------------------------------------------------\n");

    // 初期状態の表示
    printf("%d\t\t %.2f\t\t %.8f\t %.8f\n", 0, t, x, v);

    // 時間を進めながら10ステップ分計算 (速度ベルレ法)
    for (int i = 1; i <= num_steps; i++) {
        // 1. 速度を h/2 だけ進める
        v = v + a * h / 2.0;

        // 2. 位置を h だけ進める (h/2進めた速度を使う)
        x = x + v * h;

        // 3. 新しい位置 x(t+h) を使って、新しい加速度 a(t+h) を計算
        a = -(k / m) * x;

        // 4. 新しい加速度を使って、残りの h/2 だけ速度を進める
        v = v + a * h / 2.0;

        // 5. 時刻 t を更新
        t = t + h;

        // 6. 計算結果を表示
        printf("%d\t\t %.2f\t\t %.8f\t %.8f\n", i, t, x, v);
    }

    printf("\n--- 最終結果の比較 (t=1.0) ---\n");
    printf("速度ベルレ法:       x = %.8f\n", x);
    printf("4次ルンゲクッタ法: x = %.8f\n", 0.54030231); // 前回の結果
    printf("厳密解 (cos(1.0)):  x = %.8f\n", cos(1.0));

    return 0;
}
