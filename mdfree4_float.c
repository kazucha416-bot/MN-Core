#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int num = 4; 
int time = 3001;

int main(void){
    /* initial values */
    /* random velocity */
    float v[3][num], vmean[3];
    for(int i=0; i<3; i++){
        vmean[i] = 0.0f;
        for(int j=0; j<num; j++){ // num=4
            // 2.0 -> 2.0f, 1.0 -> 1.0f
            v[i][j] = (rand() / (float)RAND_MAX) * 2.0f - 1.0f;
            vmean[i] = vmean[i] + v[i][j];
        }
        vmean[i] = vmean[i] / (float)num;
    }

    for(int j=0; j<num; j++){ 
        v[0][j] = v[0][j] - vmean[0];
        v[1][j] = v[1][j] - vmean[1];
        v[2][j] = v[2][j] - vmean[2];
    }
    
    /* velocity scale */
    float ke, temp, temp0 = 1.0f; // 1.0f
    ke = 0.0f;
    for(int j=0; j<num; j++){ 
        // 0.5 -> 0.5f, pow -> powf
        ke += 0.5f * (powf(v[0][j], 2.0f) + powf(v[1][j], 2.0f) + powf(v[2][j], 2.0f));
    }
    ke /= (float)num;
    temp = ke / 1.5f; // 1.5f
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){ 
            // sqrt -> sqrtf
            v[i][j] *= sqrtf(temp0/temp);
        }
    }

    /* position */
    // nx, ny, nz を 1 に変更
    int a = 2, nx = 1, ny = 1, nz = 1, n = -1;
    // a/2.0 -> a/2.0f
    float pos0[3][4] = {{0.0f, 0.0f, a/2.0f, a/2.0f},
                        {0.0f, a/2.0f, a/2.0f, 0.0f},
                        {0.0f, a/2.0f, 0.0f, a/2.0f}};
    float pos[3][num]; 

    // このループは 1*1*1 = 1回だけ実行される
    for(int jx=1; jx<=nx; jx++){
        for(int jy=1; jy<=ny; jy++){
            for(int jz=1; jz<=nz; jz++){
                n = n + 1; // n=0
                pos[0][n] = pos0[0][0] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][0] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][0] + (jz - 1) * (float)a;
                n = n + 1; // n=1
                pos[0][n] = pos0[0][1] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][1] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][1] + (jz - 1) * (float)a;
                n = n + 1; // n=2
                pos[0][n] = pos0[0][2] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][2] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][2] + (jz - 1) * (float)a;
                n = n + 1; // n=3
                pos[0][n] = pos0[0][3] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][3] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][3] + (jz - 1) * (float)a;
            }
        }
    }

    /* force & potential energy*/
    float x, y, z, r2, r2i, r06i, r12i, ep, engp, fc, fx, fy, fz, force1[3][num], force2[3][num];
    float dt, eps, sigma, ce12, ce06, cf12, cf06;
    
    // 定数にfを追加
    dt = 0.001f;
    eps = 1.0f;
    sigma = 1.0f;
    // pow -> powf, 12 -> 12.0f
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

    // 4個の粒子（n=0,1,2,3）で力計算
    for(int j=1; j<num; j++){ 
        for(int i=0; i<j; i++){ 
            x = pos[0][i] - pos[0][j];
            y = pos[1][i] - pos[1][j];
            z = pos[2][i] - pos[2][j];
            r2 = x*x + y*y + z*z;
            r2i = 1.0f / r2; // 1 -> 1.0f
            r06i = powf(r2i, 3.0f); // pow -> powf
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
            // 0.5 -> 0.5f
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
                r06i = r2i * r2i * r2i;
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
    e = fopen("/home/kazuki/mncore/0113mdfree4_cpu_result_float_3000.txt", "w");
    for(int k=0; k<time; k++){
        fprintf(e, "%f\t%f\t%f\t%f\n", dt*(float)k, engp_value[k], ke_value[k], total_value[k]);
    }
    fclose(e);

    return 0;
}