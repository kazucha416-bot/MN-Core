import struct
import subprocess
import numpy as np
import os

def float_to_mn_hex(val):
    """
    float数値をMN-Core用の16進数表記文字列に変換する関数
    仕様: 単精度(32bit)の16進数 + ゼロ8個
    例: 2.0 -> '40000000' + '00000000' -> '4000000000000000'
    """
    # 単精度浮動小数点数(float)としてパックし、hex文字列化
    float_hex = struct.pack('>f', val).hex()
    # 後ろにゼロを8個つける
    return float_hex + "00000000"

def run_experiment():
    # --- 設定 ---
    template_vsm = "LJ_force_plot_forthesis.vsm" # 元のファイル
    temp_vsm = "temp_experiment.vsm"             # 一時ファイル
    temp_asm = "temp_experiment.asm"             # アセンブル後のファイル
    
    # ターゲットとする命令のキーワード（この行を探して書き換えます）
    target_keyword = "d set $lm0n0c0b0m0p0 1"

    # 距離 r の範囲設定 (0.5 から 3.0 まで 0.1 刻み)
    # np.arange(start, stop, step) だと誤差が出ることがあるので、整数で回して割るのが安全
    r_values = [x / 10.0 for x in range(5, 31)] # 5, 6, ..., 30 -> 0.5, 0.6, ..., 3.0

    print(f"🚀 実験開始: r = {r_values[0]} -> {r_values[-1]} ({len(r_values)} patterns)")

    # 元のファイルを読み込む
    with open(template_vsm, 'r') as f:
        lines = f.readlines()

    # --- ループ実行 ---
    for r in r_values:
        # 1. 値の変換
        hex_val = float_to_mn_hex(r)
        
        # 2. VSMファイルの書き換え
        new_lines = []
        replaced = False
        for line in lines:
            if line.strip().startswith(target_keyword):
                # 書き換え: "d set $lm0... 1 <HEX>\n"
                new_line = f"{target_keyword} {hex_val}\n"
                new_lines.append(new_line)
                replaced = True
            else:
                new_lines.append(line)
        
        if not replaced:
            print(f"⚠️ 警告: キーワード '{target_keyword}' が見つかりませんでした。スキップします。")
            break

        # 一時VSMファイルに保存
        with open(temp_vsm, 'w') as f:
            f.writelines(new_lines)

        # 3. アセンブル (assemble3)
        # cmd: assemble3 temp.vsm > temp.asm
        try:
            subprocess.run(f"assemble3 {temp_vsm} > {temp_asm}", shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"❌ アセンブルエラー (r={r})")
            continue

        # 4. 実行 (gpfn3_package_main)
        # 結果ファイル名: dumps/result_r_1.5.dmp など
        output_dir = "dumps"
        os.makedirs(output_dir, exist_ok=True)
        dump_file = os.path.join(output_dir, f"result_r_{r:.1f}.dmp")
        
        try:
            subprocess.run(["gpfn3_package_main", "-i", temp_asm, "-d", dump_file], check=True)
            print(f"✅ r={r:.1f} : 完了 -> {dump_file}")
        except subprocess.CalledProcessError:
            print(f"❌ 実行エラー (r={r})")

    # 後始末（一時ファイルの削除）
    if os.path.exists(temp_vsm): os.remove(temp_vsm)
    if os.path.exists(temp_asm): os.remove(temp_asm)
    
    print("🎉 全パターンの実験が終了しました！")

if __name__ == "__main__":
    run_experiment()