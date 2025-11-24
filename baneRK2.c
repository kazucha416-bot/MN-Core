#include <stdio.h>

int main() {
    // パラメータの設定 (単精度 float)
    const float h = 0.1f;   // 時間の刻み幅 (time step)
    const float k = 1.0f;   // ばね定数 (spring constant)
    const float m = 1.0f;   // 質量 (mass)

    // 初期条件
    float x = 1.0f;   // 初期位置 (initial position, x_0)
    float v = 0.0f;   // 初期速度 (initial velocity, v_0)
    float t = 0.0f;   // 初期時刻 (initial time)

    // 計算するステップ数
    const int num_steps = 70;

    // ヘッダー（見出し）の表示
    printf("ステップ\t 時刻 t\t\t 位置 x\t\t 速度 v\n");
    printf("----------------------------------------------------------\n");

    // 初期状態の表示
    printf("%d\t\t %.2f\t\t %.6f\t %.6f\n", 0, t, x, v);

    // 時間を進めながら10ステップ分計算 (2次のルンゲ＝クッタ法)
    for (int i = 1; i <= num_steps; i++) {
        // --- 2次のルンゲ＝クッタ法 ---

        // 1. 中間点(h/2)での速度と位置を予測計算する
        float a_current = -(k / m) * x;           // 現在の加速度
        float v_mid = v + a_current * (h / 2.0f); // 中間点の速度 v(t + h/2)
        float x_mid = x + v * (h / 2.0f);         // 中間点の位置 x(t + h/2)

        // 2. 中間点の位置を使って、中間点での加速度を計算する
        float a_mid = -(k / m) * x_mid;           // 中間点の加速度 a(t + h/2)

        // 3. 中間点の速度と加速度を使って、次のステップの値を更新する
        v = v + a_mid * h;   // v(t+h) = v(t) + a_mid * h
        x = x + v_mid * h;   // x(t+h) = x(t) + v_mid * h

        // 4. 時刻 t を更新
        t = t + h;

        // 5. 計算結果を表示
        printf("%d\t\t %.2f\t\t %.6f\t %.6f\n", i, t, x, v);
    }

    return 0;
}
