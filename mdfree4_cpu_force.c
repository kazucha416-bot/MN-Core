#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int num = 4; 
int time = 3001; // ステップ数

int main(void){
    /* initial values */
    /* random velocity */
    float v[3][num], vmean[3];
    for(int i=0; i<3; i++){
        vmean[i] = 0.0f;
        for(int j=0; j<num; j++){ // num=4
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
    float ke, temp, temp0 = 1.0f;
    ke = 0.0f;
    for(int j=0; j<num; j++){ 
        ke += 0.5f * (powf(v[0][j], 2.0f) + powf(v[1][j], 2.0f) + powf(v[2][j], 2.0f));
    }
    ke /= (float)num;
    temp = ke / 1.5f;
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){ 
            v[i][j] *= sqrtf(temp0/temp);
        }
    }

    /* position */
    int a = 2, nx = 1, ny = 1, nz = 1, n = -1;
    float pos0[3][4] = {{0.0f, 0.0f, a/2.0f, a/2.0f},
                        {0.0f, a/2.0f, a/2.0f, 0.0f},
                        {0.0f, a/2.0f, 0.0f, a/2.0f}};
    float pos[3][num]; 

    for(int jx=1; jx<=nx; jx++){
        for(int jy=1; jy<=ny; jy++){
            for(int jz=1; jz<=nz; jz++){
                n = n + 1;
                pos[0][n] = pos0[0][0] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][0] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][0] + (jz - 1) * (float)a;
                n = n + 1;
                pos[0][n] = pos0[0][1] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][1] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][1] + (jz - 1) * (float)a;
                n = n + 1;
                pos[0][n] = pos0[0][2] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][2] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][2] + (jz - 1) * (float)a;
                n = n + 1;
                pos[0][n] = pos0[0][3] + (jx - 1) * (float)a;
                pos[1][n] = pos0[1][3] + (jy - 1) * (float)a;
                pos[2][n] = pos0[2][3] + (jz - 1) * (float)a;
            }
        }
    }

    /* force & potential energy parameters */
    float x, y, z, r2, r2i, r06i, r12i, ep, engp, fc, fx, fy, fz, force1[3][num], force2[3][num];
    float dt, eps, sigma, ce12, ce06, cf12, cf06;
    
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

    // Initial Force Calculation (t=0)
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
            force1[0][i] += fx;
            force1[1][i] += fy;
            force1[2][i] += fz;
            force1[0][j] -= fx;
            force1[1][j] -= fy;
            force1[2][j] -= fz;
        }
    }
    
    /* Variables for Logging */
    float mas[num]; 
    float engp_value[time], total_value[time], ke_value[time];
    // ★ 力の履歴保存用配列 [ステップ][次元][粒子ID]
    float force_log[time][3][num];

    for(int j=0; j<num; j++){ 
        mas[j] = 1.0f;
    }
    
    // Main Loop
    for(int k=0; k<time; k++){
        /* position update (Verlet step 1) */
        for(int j=0; j<num; j++){ 
            pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5f * dt * dt / mas[j] * force1[0][j];
            pos[1][j] = pos[1][j] + dt * v[1][j] + 0.5f * dt * dt / mas[j] * force1[1][j];
            pos[2][j] = pos[2][j] + dt * v[2][j] + 0.5f * dt * dt / mas[j] * force1[2][j];
        }
        
        /* force calculation (at new position) */
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
                force2[0][i] += fx;
                force2[1][i] += fy;
                force2[2][i] += fz;
                force2[0][j] -= fx;
                force2[1][j] -= fy;
                force2[2][j] -= fz;
            }
        }

        // ★ ここで計算された力を記録 (ステップkの力として保存)
        for(int j=0; j<num; j++){
            force_log[k][0][j] = force2[0][j];
            force_log[k][1][j] = force2[1][j];
            force_log[k][2][j] = force2[2][j];
        }
        
        /* velocity update (Verlet step 2) */
        for(int j=0; j<num; j++){ 
            v[0][j] = v[0][j] + 0.5f * dt / mas[j] * (force1[0][j] + force2[0][j]);
            v[1][j] = v[1][j] + 0.5f * dt / mas[j] * (force1[1][j] + force2[1][j]);
            v[2][j] = v[2][j] + 0.5f * dt / mas[j] * (force1[2][j] + force2[2][j]);
        }
        
        // Kinetic Energy
        ke = 0.0f;
        for(int j=0; j<num; j++){ 
            ke += 0.5f * (powf(v[0][j], 2.0f) + powf(v[1][j], 2.0f) + powf(v[2][j], 2.0f));
        }
        ke /= (float)num; 

        // Update forces for next step
        for(int i=0; i<3; i++){
            for(int j=0; j<num; j++){ 
                force1[i][j] = force2[i][j];
                force2[i][j] = 0.0f; // Reset buffer
            }
        }

        engp_value[k] = engp;
        ke_value[k] = ke * (float)num; 
        total_value[k] = ke_value[k] + engp_value[k];
    }
    
    // --- File Output (Energy) ---
    FILE *e;
    e = fopen("/home/kazuki/mncore/mdfree4_cpu_result_float.txt", "w");
    if(e == NULL){ printf("Error opening energy file.\n"); return 1; }
    for(int k=0; k<time; k++){
        fprintf(e, "%f\t%f\t%f\t%f\n", dt*(float)k, engp_value[k], ke_value[k], total_value[k]);
    }
    fclose(e);

    // --- File Output (Forces) ---
    // Output Format: Time, Fx0, Fy0, Fz0, Fx1, Fy1, Fz1, ...
    FILE *f_force;
    f_force = fopen("/home/kazuki/mncore/mdfree4_cpu_force.txt", "w");
    if(f_force == NULL){ printf("Error opening force file.\n"); return 1; }
    
    for(int k=0; k<time; k++){
        fprintf(f_force, "%f", dt*(float)k);
        for(int j=0; j<num; j++){
            fprintf(f_force, "\t%e\t%e\t%e", 
                    force_log[k][0][j], 
                    force_log[k][1][j], 
                    force_log[k][2][j]);
        }
        fprintf(f_force, "\n");
    }
    fclose(f_force);
    printf("Force data saved to mdfree4_cpu_force.txt\n");

    return 0;
}