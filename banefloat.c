#include <stdio.h>

int main() {
    // ======== 単精度 (float) の計算 ========
    printf("--- Single Precision (float) ---\n");
    const float h_f = 0.0001f;
    const float k_f = 1.0f;
    const float m_f = 1.0f;
    float x_f = 1.0f;
    float v_f = 0.0f;
    float t_f = 0.0f;
    const int num_steps = 70000; // ステップ数

    printf("Step\t Time\t\t Position x (float)\t Velocity v (float)\n");
    printf("---------------------------------------------------------------\n");
    printf("%d\t %.2f\t\t %.8f\t %.8f\n", 0, t_f, x_f, v_f); // 初期値表示

    for (int i = 1; i <= num_steps; i++) {
        float a_f = -(k_f / m_f) * x_f;
        v_f = v_f + a_f * h_f;
        x_f = x_f + v_f * h_f;
        t_f = t_f + h_f;
        if (i % 10000 == 0) { // 10ステップごとに表示（位置と速度）
             printf("%d\t %.2f\t\t %.8f\t %.8f\n", i, t_f, x_f, v_f);
        }
    }

    return 0;
}
