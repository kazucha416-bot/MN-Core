#include <stdio.h>
#include <math.h>

#define N 1000         // ステップ数
#define DT 0.01        // 時間刻み
#define K 1.0          // ばね定数 [N/m]
#define M 1.0          // 質量 [kg]

int main(void) {
    double x[N], v[N], a, a_next, t[N];
    int i;

    // 初期条件
    x[0] = 1.0;    // 初期位置 [m]
    v[0] = 0.0;    // 初速度 [m/s]
    t[0] = 0.0;

    // 速度ベルレ法で計算
    for (i = 0; i < N - 1; i++) {
        t[i+1] = t[i] + DT;
        a = -K * x[i] / M;
        x[i+1] = x[i] + v[i] * DT + 0.5 * a * DT * DT;
        a_next = -K * x[i+1] / M;
        v[i+1] = v[i] + 0.5 * (a + a_next) * DT;
    }

    // 結果を出力（CSV形式：時間,位置,速度）
    printf("time,position,velocity\n");
    for (i = 0; i < N; i++) {
        printf("%f,%f,%f\n", t[i], x[i], v[i]);
    }

    return 0;
}
