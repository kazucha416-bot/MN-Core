#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int num = 4; 
int time = 3001;

int main(void){
    
    // =========================================================
    // 1. 初期速度の手動入力エリア
    // =========================================================
    float v_init[3][4] = {
        // 粒子0,   粒子1,   粒子2,   粒子3
        {  -0.484558f,  0.0252283f,   0.28812f,   0.171209f }, // vx
        {  -0.613818f,   0.584736f,   0.135554f,  -0.106472f }, // vy
        {  -0.636838f,  0.253943f,   0.708598f,  -0.325703f }  // vz
    };

    float v[3][num];
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){
            v[i][j] = v_init[i][j];
        }
    }

    // =========================================================
    // 2. 初期配置 (粒子0を原点に置く正四面体配置)
    // =========================================================
    float r = powf(2.0f, -1.0f/3.0f);
    
    float pos[3][4] = {
        {   0.0f,   0.0f,           r,           r },             // x
        {   0.0f,      r,           r,        0.0f }, // y
        {   0.0f,      r,        0.0f,           r }  // z
    };

    /* force & potential energy*/
    float x, y, z, r2, r2i, r06i, r12i, ep, engp, fc, fx, fy, fz, force1[3][num], force2[3][num];
    float dt, eps, sigma, ce12, ce06, cf12, cf06;
    float ke; 
    
    dt = 0.001f;
    eps = 1.0f;
    sigma = 1.0f;
    
    ce12 = 4.0f * eps * powf(sigma, 12.0f);
    ce06 = 4.0f * eps * powf(sigma, 6.0f);
    cf12 = ce12 * 12.0f;
    cf06 = ce06 * 6.0f;
    
    engp = 0.0f;
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){ 
            force1[i][j] = 0.0f;
            force2[i][j] = 0.0f;
        }
    }

    // 初回の力計算
    for(int j=1; j<num; j++){ 
        for(int i=0; i<j; i++){ 
            x = pos[0][i] - pos[0][j];
            y = pos[1][i] - pos[1][j];
            z = pos[2][i] - pos[2][j];
            r2 = x*x + y*y + z*z;
            r2i = 1.0f / r2;
            r06i = powf(r2i, 3.0f);
            r12i = r06i * r06i;
            ep = ce12 * r12i - ce06 * r06i;
            engp = engp + ep;
            fc = (cf12 * r12i - cf06 * r06i) * r2i;
            fx = fc * x;
            fy = fc * y;
            fz = fc * z;
            force1[0][i] = force1[0][i] + fx;
            force1[1][i] = force1[1][i] + fy;
            force1[2][i] = force1[2][i] + fz;
            force1[0][j] = force1[0][j] - fx;
            force1[1][j] = force1[1][j] - fy;
            force1[2][j] = force1[2][j] - fz;
        }
    }
    
    /*calculation*/
    float mas[num]; 
    float engp_value[time], total_value[time], ke_value[time];
    
    for(int j=0; j<time; j++){
        engp_value[j] = 0.0f;
        ke_value[j] = 0.0f;
        total_value[j] = 0.0f;
    }

    for(int j=0; j<num; j++){ 
        mas[j] = 1.0f;
    }
    
    for(int k=0; k<time; k++){
        /* position */
        for(int j=0; j<num; j++){ 
            pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5f * dt * dt / mas[j] * force1[0][j];
            pos[1][j] = pos[1][j] + dt * v[1][j] + 0.5f * dt * dt / mas[j] * force1[1][j];
            pos[2][j] = pos[2][j] + dt * v[2][j] + 0.5f * dt * dt / mas[j] * force1[2][j];
        }
        
        /* force */
        engp = 0.0f;
        for(int j=1; j<num; j++){ 
            for(int i=0; i<j; i++){
                x = pos[0][i] - pos[0][j];
                y = pos[1][i] - pos[1][j];
                z = pos[2][i] - pos[2][j];
                r2 = x*x + y*y + z*z;
                r2i = 1.0f / r2;
                r06i = powf(r2i, 3.0f);
                r12i = r06i * r06i;
                ep = ce12 * r12i - ce06 * r06i;
                engp = engp + ep;
                fc = (cf12 * r12i - cf06 * r06i) * r2i;
                fx = fc * x;
                fy = fc * y;
                fz = fc * z;
                force2[0][i] = force2[0][i] + fx;
                force2[1][i] = force2[1][i] + fy;
                force2[2][i] = force2[2][i] + fz;
                force2[0][j] = force2[0][j] - fx;
                force2[1][j] = force2[1][j] - fy;
                force2[2][j] = force2[2][j] - fz;
            }
        }
        
        /* Update Velocity */
        for(int j=0; j<num; j++){ 
            v[0][j] = v[0][j] + 0.5f * dt / mas[j] * (force1[0][j] + force2[0][j]);
            v[1][j] = v[1][j] + 0.5f * dt / mas[j] * (force1[1][j] + force2[1][j]);
            v[2][j] = v[2][j] + 0.5f * dt / mas[j] * (force1[2][j] + force2[2][j]);
        }
        
        ke = 0.0f;
        for(int j=0; j<num; j++){ 
            ke += 0.5f * (powf(v[0][j], 2.0f) + powf(v[1][j], 2.0f) + powf(v[2][j], 2.0f));
        }
        
        ke /= (float)num; 

        for(int i=0; i<3; i++){
            for(int j=0; j<num; j++){ 
                force1[i][j] = force2[i][j];
                force2[i][j] = 0.0f;
            }
        }

        engp_value[k] = engp;
        ke_value[k] = ke * (float)num; 
        total_value[k] = ke_value[k] + engp_value[k];
    }
    
    FILE *e;
    e = fopen("0216_mdfree4_cpu.txt", "w");
    
    // ★ここを変更: 10ステップごと (0.01sごと) に出力
    // dt = 0.001 なので、10 * dt = 0.01
    for(int k=0; k<time; k+=10){
        fprintf(e, "%.9g\t%.9g\t%.9g\t%.9g\n", dt*(float)k, engp_value[k], ke_value[k], total_value[k]);
    }
    fclose(e);

    return 0;
}