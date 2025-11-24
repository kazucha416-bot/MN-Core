#include <stdio.h>
#include <math.h>
#include <stdlib.h>

int num = 256;
int time = 1000;

int main(void){
/* initial values */
	/* random velocity */
	float v[3][num], vmean[3];
	for(int i=0; i<3; i++){
			vmean[i] = 0;
			for(int j=0; j<num; j++){
					v[i][j] = (rand() / (float)RAND_MAX) * 2.0 - 1.0;	/*-1.0 〜 1.0 の乱数で初期速度を設定*/
					vmean[i] = vmean[i] + v[i][j];	/*その方向の全粒子の速度の合計を計算*/
			}
			vmean[i] = vmean[i] / num;	/*各方向の平均速度（= 中心の移動速度）を求める*/
		}
        /*全粒子から平均速度を引くことで，全粒子の速度を合計した時にゼロになるようにしている．重心の移動をキャンセルしている．*/
		for(int j=0; j<num; j++){
				v[0][j] = v[0][j] - vmean[0];
				v[1][j] = v[1][j] - vmean[1];
				v[2][j] = v[2][j] - vmean[2];

		}




		/* velocity scale */      /*前のステップで設定した粒子の速度が，シミュレーションで設定したい目標温度になるように速度全体を調整する処理．*/
        /*現在の系の温度を測り，それが目標温度1.0になるように，全粒子の速度を強制的に拡大・縮小するというシミュレーションの初期設定を行っている*/
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





			/* position 粒子の配列．FCC.3重ループで256個の粒子を配置している．*/
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

			/* force & potential energy LJポテンシャルを設定し，力を計算．*/
			float x, y, z, r2, r2i, r06i, r12i, ep, engp, fc, fx, fy, fz, force1[3][num], force2[3][num];
			float dt, eps, sigma, ce12, ce06, cf12, cf06;
			dt = 0.005;
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
            /*全粒子のペアについて，2粒子間に働く力とポテンシャルエネルギーを計算し，各粒子に蓄積する(一番のかなめ)*/
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

			/*calculation　「現在の位置，現在の速度，現在の力」を使って，全粒子の「次の時刻の位置」を計算する処理*/
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
			for(int k=0; k<time; k++){
					/* position */
					for(int j=0; j<num; j++){
							 		pos[0][j] = pos[0][j] + dt * v[0][j] + 0.5 * dt * dt / mas[j] * force1[0][j];
									pos[1][j] = pos[1][j] + dt * v[1][j] + 0.5 * dt * dt / mas[j] * force1[1][j];
									pos[2][j] = pos[2][j] + dt * v[2][j] + 0.5 * dt * dt / mas[j] * force1[2][j];
					}

					/* force 位置の更新で得られた新しい位置を使ってその新しい位置における新しい力を計算する*/
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
							v[0][j] = v[0][j] + 0.5 * dt / mas[j] * (force1[0][j] + force2[0][j]);
							v[1][j] = v[1][j] + 0.5 * dt / mas[j] * (force1[1][j] + force2[1][j]);
							v[2][j] = v[2][j] + 0.5 * dt / mas[j] * (force1[2][j] + force2[2][j]);
					}
					for(int j=0; j<num; j++){
					        ke += 0.5 * (pow(v[0][j],2)+pow(v[1][j],2)+pow(v[2][j],2));
					}
					ke /= num;   /*合計の運動エネルギーを粒子の数で割って，粒子一個当たりの平均運動エネルギーを算出する*/

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
			e = fopen("/home/kazuki/mncore/MD_FBC_data.txt", "w");
			for(int k=0; k<time; k++){
					fprintf(e, "%f\t%f\t%f\t%f\n", dt*k, engp_value[k], ke_value[k], total_value[k]);
			}

			fclose(e);

			return 0;
}
