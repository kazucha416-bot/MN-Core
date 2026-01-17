#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int num = 256;
int time = 1000;
// 動径分布関数用の設定
#define BIN_SIZE 100 // ビンの数
float SL = 8.0;      // シミュレーションボックスの一辺の長さ (nx * a = 4 * 2 = 8.0)

int main(void){
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

    /* position */
    int a = 2, nx = 4, ny = 4, nz = 4, n = -1;
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

    /* RDF用の変数定義 */
    float rdf_hist[BIN_SIZE]; // ヒストグラム配列
    for(int i=0; i<BIN_SIZE; i++) rdf_hist[i] = 0.0;
    
    // RDFのカットオフ距離はボックスの半分まで (L/2)
    float rdf_max_r = SL / 2.0;
    float dr = rdf_max_r / BIN_SIZE; // ビンの幅 (dr)

    /* force & potential energy */
    float x, y, z, r2, r2i, r06i, r12i, ep, engp, fc, fx, fy, fz, force1[3][num], force2[3][num];
    float dt, eps, sigma, ce12, ce06, cf12, cf06;
    float SL2 = SL / 2.0; // 周期境界計算用 (L/2)

    dt = 0.005;
    eps = 1.0;
    sigma = 1.0;
    ce12 = 4 * eps * pow(sigma, 12);
    ce06 = 4 * eps * pow(sigma, 6);
    cf12 = ce12 * 12;
    cf06 = ce06 * 6;
    engp = 0.0;
    
    // --- 初期力計算（周期境界対応） ---
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
            
            // 最小イメージ規約 (周期境界条件) 
            if(x > SL2) x -= SL; else if(x < -SL2) x += SL;
            if(y > SL2) y -= SL; else if(y < -SL2) y += SL;
            if(z > SL2) z -= SL; else if(z < -SL2) z += SL;

            r2 = x*x + y*y + z*z;
            r2i = 1/r2;
            r06i = pow(r2i, 3);
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

    /* calculation */
    float mas[num];
    float engp_value[time], total_value[time], ke_value[time];
    for(int j=0; j<time; j++){
        engp_value[j] = 0.0;
        ke_value[j] = 0.0;
        total_value[j] = 0.0;
    }

    for(int j=0; j<num; j++){
        mas[j] = 1;
    }

    // --- メインループ ---
    for(int k=0; k<time; k++){
        /* position update & wrapping */
        for(int j=0; j<num; j++){
             pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5 * dt * dt / mas[j] * force1[0][j];
             pos[1][j] = pos[1][j] + dt * v[1][j] + 0.5 * dt * dt / mas[j] * force1[1][j];
             pos[2][j] = pos[2][j] + dt * v[2][j] + 0.5 * dt * dt / mas[j] * force1[2][j];
             
             // 周期境界による折り返し処理 
             if(pos[0][j] >= SL) pos[0][j] -= SL; else if(pos[0][j] < 0) pos[0][j] += SL;
             if(pos[1][j] >= SL) pos[1][j] -= SL; else if(pos[1][j] < 0) pos[1][j] += SL;
             if(pos[2][j] >= SL) pos[2][j] -= SL; else if(pos[2][j] < 0) pos[2][j] += SL;
        }

        /* force calculation (at new position) */
        engp = 0.0;
        for(int j=1; j<num; j++){
            for(int i=0; i<j; i++){
                x = pos[0][i] - pos[0][j];
                y = pos[1][i] - pos[1][j];
                z = pos[2][i] - pos[2][j];
                
                // 最小イメージ規約
                if(x > SL2) x -= SL; else if(x < -SL2) x += SL;
                if(y > SL2) y -= SL; else if(y < -SL2) y += SL;
                if(z > SL2) z -= SL; else if(z < -SL2) z += SL;

                r2 = x*x + y*y + z*z;
                r2i = 1/r2;
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

                // --- RDFのサンプリング [cite: 85, 95] ---
                // 力計算のループ内で距離計算済みの r2 を利用する
                float r = sqrt(r2);
                if (r < rdf_max_r) {
                    int bin_index = (int)(r / dr); // いくつ目のdrの場所にあるか [cite: 91]
                    if (bin_index < BIN_SIZE) {
                        rdf_hist[bin_index] += 2.0; // iとjの両方分カウント 
                    }
                }
            }
        }
        
        /* Update Velocity */
        for(int j=0; j<num; j++){
            v[0][j] = v[0][j] + 0.5 * dt / mas[j] * (force1[0][j] + force2[0][j]);
            v[1][j] = v[1][j] + 0.5 * dt / mas[j] * (force1[1][j] + force2[1][j]);
            v[2][j] = v[2][j] + 0.5 * dt / mas[j] * (force1[2][j] + force2[2][j]);
        }
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

    // --- エネルギーの出力 ---
    FILE *e;
    e = fopen("MD_PBC_energy.txt", "w");
    for(int k=0; k<time; k++){
        fprintf(e, "%f\t%f\t%f\t%f\n", dt*k, engp_value[k], ke_value[k], total_value[k]);
    }
    fclose(e);

    // --- 動径分布関数 g(r) の計算と出力  ---
    FILE *gr;
    gr = fopen("MD_PBC_RDF.txt", "w");
    
    float rho = num / (SL * SL * SL); // 平均密度 rho [cite: 68]
    float PI = 3.1415926535;

    for(int i=0; i<BIN_SIZE; i++){
        float r = (i + 0.5) * dr; // ビンの中心距離 r [cite: 80]
        
        // 球殻の体積 dV = 4 * pi * r^2 * dr [cite: 77]
        float dV = 4.0 * PI * r * r * dr;
        
        // 理想気体の場合の粒子数 dn_ideal = rho * dV
        float dn_ideal = rho * dV;

        // 時間平均した粒子数 <n(r)>
        // rdf_histは全ステップ・全粒子の合計なので、(time * num) で割る
        float n_obs = rdf_hist[i] / (float)(time * num);

        // g(r) = <n(r)> / (rho * 4 * pi * r^2 * dr)
        float g_r = n_obs / dn_ideal;

        fprintf(gr, "%f\t%f\n", r, g_r);
    }
    fclose(gr);

    return 0;
}