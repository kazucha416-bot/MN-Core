#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int num = 256;
int time_steps = 1000; // 変数名 time は time.h と競合しやすいため変更

int main(void){
    /* Simulation Box Parameters */
    /* FCC 4x4x4, Lattice constant a=2.0 -> Box Size L=8.0 */
    int nx = 4, ny = 4, nz = 4;
    float a = 2.0;
    float L = nx * a;       // シミュレーションボックスの一辺の長さ (8.0)
    float half_L = L / 2.0; // 最小イメージ法で使う L/2 (4.0)

    /* initial values */
    /* random velocity */
    float v[3][num], vmean[3];
    for(int i=0; i<3; i++){
        vmean[i] = 0;
        for(int j=0; j<num; j++){
            v[i][j] = (rand() / (float)RAND_MAX) * 2.0 - 1.0;
            vmean[i] = vmean[i] + v[i][j];
        }
        vmean[i] = vmean[i] / num;
    }

    for(int j=0; j<num; j++){
        v[0][j] = v[0][j] - vmean[0];
        v[1][j] = v[1][j] - vmean[1];
        v[2][j] = v[2][j] - vmean[2];
    }

    /* velocity scale */
    float ke, temp, temp0 = 1.0;
    ke = 0.0;
    for(int j=0; j<num; j++){
        ke +=  0.5 * (pow(v[0][j],2)+pow(v[1][j],2)+pow(v[2][j],2));
    }
    ke /= num;
    temp = ke / 1.5;
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){
            v[i][j] *= sqrt(temp0/temp);
        }
    }

    /* position (FCC Lattice) */
    int n = -1;
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
    dt = 0.005;
    eps = 1.0;
    sigma = 1.0;
    ce12 = 4 * eps * pow(sigma, 12);
    ce06 = 4 * eps * pow(sigma, 6);
    cf12 = ce12 * 12;
    cf06 = ce06 * 6;
    
    // --- 初期力計算 (Force 1) ---
    engp = 0.0;
    for(int i=0; i<3; i++){
        for(int j=0; j<num; j++){
            force1[i][j] = 0;
            force2[i][j] = 0;
        }
    }
    for(int j=1; j<num; j++){
        for(int i=0; i<j; i++){
            x = pos[0][i] - pos[0][j];
            y = pos[1][i] - pos[1][j];
            z = pos[2][i] - pos[2][j];

            /* ★変更点1: 最小イメージ法 (Minimum Image Convention) */
            if (x > half_L) x -= L;
            else if (x < -half_L) x += L;
            
            if (y > half_L) y -= L;
            else if (y < -half_L) y += L;
            
            if (z > half_L) z -= L;
            else if (z < -half_L) z += L;
            /* -------------------------------------------------- */

            r2 = x*x + y*y + z*z;
            
            // (カットオフを入れるならここで if(r2 < cutoff2) を入れるが、今回は全ペア計算)
            
            r2i = 1/r2;
            r06i = pow(r2i, 3);
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

    /* calculation */
    float mas[num];
    float engp_value[time_steps], total_value[time_steps], ke_value[time_steps];
    
    // 配列初期化 (元のコードのバグ修正: j<num -> j<time_steps)
    for(int j=0; j<time_steps; j++){
        engp_value[j] = 0.0;
        ke_value[j] = 0.0;
        total_value[j] = 0.0;
    }

    for(int j=0; j<num; j++){
        mas[j] = 1;
    }
    
    // --- メインループ ---
    for(int k=0; k<time_steps; k++){
        
        /* position update */
        for(int j=0; j<num; j++){
            pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5 * dt * dt / mas[j] * force1[0][j];
            pos[1][j] = pos[1][j] + dt * v[1][j] + 0.5 * dt * dt / mas[j] * force1[1][j];
            pos[2][j] = pos[2][j] + dt * v[2][j] + 0.5 * dt * dt / mas[j] * force1[2][j];
            
            /* ★変更点2: 周期境界条件による位置の折り返し (Wrapping) */
            if (pos[0][j] < 0.0) pos[0][j] += L;
            else if (pos[0][j] >= L) pos[0][j] -= L;

            if (pos[1][j] < 0.0) pos[1][j] += L;
            else if (pos[1][j] >= L) pos[1][j] -= L;

            if (pos[2][j] < 0.0) pos[2][j] += L;
            else if (pos[2][j] >= L) pos[2][j] -= L;
            /* ------------------------------------------------------ */
        }

        /* force calculation (Force 2) */
        engp = 0.0;
        for(int j=1; j<num; j++){
            for(int i=0; i<j; i++){
                x = pos[0][i] - pos[0][j];
                y = pos[1][i] - pos[1][j];
                z = pos[2][i] - pos[2][j];

                /* ★変更点1: 最小イメージ法 (ここも同様に追加) */
                if (x > half_L) x -= L;
                else if (x < -half_L) x += L;
                
                if (y > half_L) y -= L;
                else if (y < -half_L) y += L;
                
                if (z > half_L) z -= L;
                else if (z < -half_L) z += L;
                /* ---------------------------------------- */

                r2 = x*x + y*y + z*z;
                
                r2i = 1/r2;
                r06i = r2i * r2i * r2i; // powより高速
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

        /* Update Velocity */
        ke = 0.0; // ループ内でリセットが必要
        for(int j=0; j<num; j++){
            v[0][j] = v[0][j] + 0.5 * dt / mas[j] * (force1[0][j] + force2[0][j]);
            v[1][j] = v[1][j] + 0.5 * dt / mas[j] * (force1[1][j] + force2[1][j]);
            v[2][j] = v[2][j] + 0.5 * dt / mas[j] * (force1[2][j] + force2[2][j]);
        }
        for(int j=0; j<num; j++){
            ke += 0.5 * (pow(v[0][j],2)+pow(v[1][j],2)+pow(v[2][j],2));
        }
        ke /= num;

        /* Prepare for next step */
        for(int i=0; i<3; i++){
            for(int j=0; j<num; j++){
                force1[i][j] = force2[i][j];
                force2[i][j] = 0;
            }
        }
        
        engp_value[k] = engp;
        ke_value[k] = ke;
        total_value[k] = (engp / num) + ke; // ポテンシャルも粒子あたりに直して合計
    }

    FILE *e;
    e = fopen("/home/kazuki/mncore/md_pbc.txt", "w");
    for(int k=0; k<time_steps; k++){
        fprintf(e, "%f\t%f\t%f\t%f\n", dt*k, engp_value[k]/num, ke_value[k], total_value[k]);
    }
    fclose(e);
    
    return 0;
}
