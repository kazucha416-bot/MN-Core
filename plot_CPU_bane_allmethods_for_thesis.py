import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    # --- 設定 ---
    # 保存先ディレクトリ
    save_dir = r'/home/kazuki/thesis/images'
    os.makedirs(save_dir, exist_ok=True)
    
    # 物理定数 (単振動モデル: F = -kx)
    k = 1.0
    m = 1.0
    
    # シミュレーション設定
    dt = 0.05       # タイムステップ
    steps = 500     # ステップ数
    t_max = dt * steps
    time = np.linspace(0, t_max, steps+1)
    
    # 初期条件 (x=1, v=0 -> E=0.5)
    x0 = 1.0
    v0 = 0.0
    # E_true = 0.5 * k * x0**2 + 0.5 * m * v0**2 # True Valueは計算だけしておく（プロットはしない）

    # --- ソルバー関数の定義 ---
    
    # 1. オイラーの陽解法 (Explicit Euler)
    def solve_euler():
        x = np.zeros(steps+1)
        v = np.zeros(steps+1)
        x[0], v[0] = x0, v0
        for i in range(steps):
            a = -(k/m) * x[i]
            x[i+1] = x[i] + v[i] * dt
            v[i+1] = v[i] + a * dt
        return x, v

    # 2. シンプレクティック・オイラー (Symplectic Euler)
    def solve_symplectic_euler():
        x = np.zeros(steps+1)
        v = np.zeros(steps+1)
        x[0], v[0] = x0, v0
        for i in range(steps):
            a = -(k/m) * x[i]
            v[i+1] = v[i] + a * dt
            x[i+1] = x[i] + v[i+1] * dt
        return x, v

    # 3. 速度ベルレ法 (Velocity Verlet)
    def solve_velocity_verlet():
        x = np.zeros(steps+1)
        v = np.zeros(steps+1)
        x[0], v[0] = x0, v0
        a = -(k/m) * x[0]
        for i in range(steps):
            x[i+1] = x[i] + v[i]*dt + 0.5*a*dt**2
            a_new = -(k/m) * x[i+1]
            v[i+1] = v[i] + 0.5*(a + a_new)*dt
            a = a_new
        return x, v

    # 4. 2次のルンゲ・クッタ (RK2)
    def solve_rk2():
        x = np.zeros(steps+1)
        v = np.zeros(steps+1)
        x[0], v[0] = x0, v0
        for i in range(steps):
            a1 = -(k/m) * x[i]
            v1 = v[i]
            x_temp = x[i] + v1 * dt
            v_temp = v[i] + a1 * dt
            a2 = -(k/m) * x_temp
            v2 = v_temp
            x[i+1] = x[i] + 0.5 * (v1 + v2) * dt
            v[i+1] = v[i] + 0.5 * (a1 + a2) * dt
        return x, v

    # 5. 4次のルンゲ・クッタ (RK4)
    def solve_rk4():
        x = np.zeros(steps+1)
        v = np.zeros(steps+1)
        x[0], v[0] = x0, v0
        for i in range(steps):
            ax1 = -(k/m) * x[i]
            vx1 = v[i]
            ax2 = -(k/m) * (x[i] + vx1 * 0.5 * dt)
            vx2 = v[i] + ax1 * 0.5 * dt
            ax3 = -(k/m) * (x[i] + vx2 * 0.5 * dt)
            vx3 = v[i] + ax2 * 0.5 * dt
            ax4 = -(k/m) * (x[i] + vx3 * dt)
            vx4 = v[i] + ax3 * dt
            x[i+1] = x[i] + (dt/6.0) * (vx1 + 2*vx2 + 2*vx3 + vx4)
            v[i+1] = v[i] + (dt/6.0) * (ax1 + 2*ax2 + 2*ax3 + ax4)
        return x, v

    # --- エネルギー計算 ---
    def calc_energy(x, v):
        return 0.5 * k * x**2 + 0.5 * m * v**2

    # 各手法の実行
    results = {}
    solvers = [
        ('Explicit Euler', solve_euler),
        ('Symplectic Euler', solve_symplectic_euler),
        ('Velocity Verlet', solve_velocity_verlet),
        ('RK2', solve_rk2),
        ('RK4', solve_rk4)
    ]

    for name, func in solvers:
        x_res, v_res = func()
        results[name] = calc_energy(x_res, v_res)

    # ==========================================
    # プロット作成
    # ==========================================
    plt.rcParams.update({'font.size': 16}) 
    
    # 共通設定関数 (True Value削除版)
    def setup_plot():
        plt.figure(figsize=(8, 5))
        plt.xlabel('Time [s]', fontsize=16)
        plt.ylabel(r'$E_{\mathrm{total}}$', fontsize=16)
        plt.tick_params(labelsize=16)
        plt.grid(True, linestyle=':', alpha=0.6)
        # plt.axhline(...) を削除しました

    # --- Graph 1: オイラー法の発散 ---
    setup_plot()
    plt.plot(time, results['Explicit Euler'], label='Explicit Euler', color='black', linestyle='--')
    plt.legend(fontsize=16, loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'Theory_Euler_Divergence.pdf'))
    print("Saved: Theory_Euler_Divergence.pdf")

    # --- Graph 2: シンプレクティック系の比較 ---
    setup_plot()
    plt.plot(time, results['Symplectic Euler'], label='Symplectic Euler', color='green', linestyle='--')
    plt.plot(time, results['Velocity Verlet'], label='Velocity Verlet', color='red', linestyle='-')
    plt.legend(fontsize=16, loc='best')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'Theory_Symplectic_Comparison.pdf'))
    print("Saved: Theory_Symplectic_Comparison.pdf")

    # --- Graph 3: ルンゲ・クッタ系の比較 ---
    setup_plot()
    plt.plot(time, results['RK2'], label='RK2', color='blue', linestyle='--')
    plt.plot(time, results['RK4'], label='RK4', color='purple', linestyle='-')
    plt.legend(fontsize=16, loc='best')
    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, 'Theory_RK_Comparison.pdf'))
    print("Saved: Theory_RK_Comparison.pdf")

if __name__ == "__main__":
    main()