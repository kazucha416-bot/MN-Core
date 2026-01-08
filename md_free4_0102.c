#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h> // 乱数初期化用

int num = 4; 
int time_steps = 1000; // 変数名をtimeから変更（標準関数との衝突回避）

int main(void){
    // 毎回異なる乱数を生成するための初期化
    srand((unsigned int)time(NULL));

    /* initial values */
    /* random velocity */
    float v[3][num], vmean[3];
    for(int i=0; i<3; i++){
        vmean[i] = 0;
        for(int j=0; j<num; j++){ // num=4
            v[i][j] = (rand() / (float)RAND_MAX) * 2.0 - 1.0;
            vmean[i] = vmean[i] + v[i][j];
        }
        vmean[i] = vmean[i] / num;
    }

    for(int j=0; j<num; j++){ // num=4
        v[0][j] = v[0][j] - vmean[0];
        v[1][j] = v[1][j] - vmean[1];
        v[2][j] = v[2][j] - vmean[2];
    }
    
    /* velocity scale */
    float ke, temp, temp0 = 1.0;
    ke = 0.0;
    for(int j=0; j<num; j++){ // num=4
        ke +=  0.5 * (pow(v[0][j],2)+pow(v[1][j],2)+pow(v[2][j],2));
    }
    ke /= num;
    temp = ke / 1.5;
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){ // num=4
            v[i][j] *= sqrt(temp0/temp);
        }
    }

    // ★★★ ここに追加: 初期速度の出力 ★★★
    printf("--- Initial Velocities (vx, vy, vz) ---\n");
    for(int j=0; j<num; j++){
        printf("Particle %d: %10.8f  %10.8f  %10.8f\n", j, v[0][j], v[1][j], v[2][j]);
    }
    printf("---------------------------------------\n");
    // ★★★★★★★★★★★★★★★★★★★★★★★

    /* position */
    int a = 2, nx = 1, ny = 1, nz = 1, n = -1;
    float pos0[3][4] = {{0, 0, a/2.0, a/2.0},
                      {0, a/2.0, a/2.0, 0},
                      {0, a/2.0, 0, a/2.0}},
          pos[3][num]; 

    for(int jx=1; jx<=nx; jx++){
        for(int jy=1; jy<=ny; jy++){
            for(int jz=1; jz<=nz; jz++){
                n = n + 1; 
                pos[0][n] = pos0[0][0] + (jx - 1) * a; 
                pos[1][n] = pos0[1][0] + (jy - 1) * a; 
                pos[2][n] = pos0[2][0] + (jz - 1) * a;
                n = n + 1; 
                pos[0][n] = pos0[0][1] + (jx - 1) * a; 
                pos[1][n] = pos0[1][1] + (jy - 1) * a; 
                pos[2][n] = pos0[2][1] + (jz - 1) * a;
                n = n + 1; 
                pos[0][n] = pos0[0][2] + (jx - 1) * a; 
                pos[1][n] = pos0[1][2] + (jy - 1) * a; 
                pos[2][n] = pos0[2][2] + (jz - 1) * a;
                n = n + 1; 
                pos[0][n] = pos0[0][3] + (jx - 1) * a; 
                pos[1][n] = pos0[1][3] + (jy - 1) * a; 
                pos[2][n] = pos0[2][3] + (jz - 1) * a;
            }
        }
    }

    /* force & potential energy*/
    float x, y, z, r2, r2i, r06i, r12i, ep, engp, fc, fx, fy, fz, force1[3][num], force2[3][num];
    float dt, eps, sigma, ce12, ce06, cf12, cf06;
    dt = 0.001;
    eps = 1.0;
    sigma = 1.0;
    ce12 = 4 * eps * pow(sigma, 12);
    ce06 = 4 * eps * pow(sigma, 6);
    cf12 = ce12 * 12;
    cf06 = ce06 * 6;
    engp = 0.0;
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){
            force1[i][j] = 0;
            force2[i][j] = 0;
        }
    }

    // 初期力の計算
    for(int j=1; j<num; j++){
        for(int i=0; i<j; i++){
            x = pos[0][i] - pos[0][j];
            y = pos[1][i] - pos[1][j];
            z = pos[2][i] - pos[2][j];
            r2 = x*x + y*y + z*z;
            r2i = 1/r2;
            r06i = pow(r2i, 3);
            r12i = r06i * r06i;
            ep = ce12 * r12i - ce06 * r06i;
            engp = engp + ep;
            fc = (cf12 * r12i - cf06 * r06i) * r2i;
            fx = fc * x; fy = fc * y; fz = fc * z;
            force1[0][i] += fx; force1[1][i] += fy; force1[2][i] += fz;
            force1[0][j] -= fx; force1[1][j] -= fy; force1[2][j] -= fz;
        }
    }
    
    /* calculation */
    float mas[num]; 
    for(int j=0; j<num; j++) mas[j] = 1;

    // メモリ確保 (スタックオーバーフロー対策)
    float *engp_value = (float*)malloc(sizeof(float) * time_steps);
    float *total_value = (float*)malloc(sizeof(float) * time_steps);
    float *ke_value = (float*)malloc(sizeof(float) * time_steps);

    if(!engp_value || !total_value || !ke_value){
        printf("Memory allocation failed\n");
        return 1;
    }
    
    for(int k=0; k<time_steps; k++){
        /* position */
        for(int j=0; j<num; j++){
            pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5 * dt * dt / mas[j] * force1[0][j];
            pos[1][j] = pos[1][j] + dt * v[1][j] + 0.5 * dt * dt / mas[j] * force1[1][j];
            pos[2][j] = pos[2][j] + dt * v[2][j] + 0.5 * dt * dt / mas[j] * force1[2][j];
        }
        
        /* force */
        engp = 0.0;
        for(int j=1; j<num; j++){
            for(int i=0; i<j; i++){
                x = pos[0][i] - pos[0][j];
                y = pos[1][i] - pos[1][j];
                z = pos[2][i] - pos[2][j];
                r2 = x*x + y*y + z*z;
                r2i = 1/r2;
                r06i = r2i * r2i * r2i;
                r12i = r06i * r06i;
                ep = ce12 * r12i - ce06 * r06i;
                engp = engp + ep;
                fc = (cf12 * r12i - cf06 * r06i) * r2i;
                fx = fc * x; fy = fc * y; fz = fc * z;
                force2[0][i] += fx; force2[1][i] += fy; force2[2][i] += fz;
                force2[0][j] -= fx; force2[1][j] -= fy; force2[2][j] -= fz;
            }
        }
        
        /* Update Velocity */
        for(int j=0; j<num; j++){
            v[0][j] = v[0][j] + 0.5 * dt / mas[j] * (force1[0][j] + force2[0][j]);
            v[1][j] = v[1][j] + 0.5 * dt / mas[j] * (force1[1][j] + force2[1][j]);
            v[2][j] = v[2][j] + 0.5 * dt / mas[j] * (force1[2][j] + force2[2][j]);
        }
        
        ke = 0.0;
        for(int j=0; j<num; j++){ 
            ke += 0.5 * (pow(v[0][j],2)+pow(v[1][j],2)+pow(v[2][j],2));
        }
        ke /= num; 

        for(int i=0; i<3; i++){
            for(int j=0; j<num; j++){
                force1[i][j] = force2[i][j];
                force2[i][j] = 0;
            }
        }

        engp_value[k] = engp;
        ke_value[k] = ke * num;
        total_value[k] = ke_value[k] + engp_value[k];
    }
    
    FILE *e;
    e = fopen("/home/kazuki/mncore/mdfree4_cpu_result_sameinitialvelocity.txt", "w");
    if (e == NULL) {
        printf("Error: Could not open file.\n");
        return 1;
    }
    for(int k=0; k<time_steps; k++){
        fprintf(e, "%f\t%f\t%f\t%f\n", dt*k, engp_value[k], ke_value[k], total_value[k]);
    }
    fclose(e);

    free(engp_value);
    free(ke_value);
    free(total_value);

    return 0;
}