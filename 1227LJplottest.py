import numpy as np
import matplotlib.pyplot as plt
import struct
import os

def main():
    # --- 設定 ---
    # 読み込むファイル名
    input_filename = '1227ljplottest.txt'
    
    # 出力するファイル名 (カレントディレクトリに保存)
    output_filename = 'lj_potential_verification.pdf'

    # rの設定
    r_start = 1.0
    dr = 0.1

    # --- 関数定義 ---
    
    # 16進数(Double) -> Float変換
    def hex_to_double(hex_str):
        # 0x, カンマ, 空白などを除去
        s = hex_str.strip().replace('0x', '').replace(',', '')
        try:
            return struct.unpack('>d', bytes.fromhex(s))[0]
        except ValueError:
            return None

    # LJポテンシャル厳密解 (epsilon=1, sigma=1)
    def lj_exact(r):
        r6_inv = (1.0 / r) ** 6
        return 4.0 * (r6_inv**2 - r6_inv)

    # --- データ読み込み処理 ---
    
    if not os.path.exists(input_filename):
        print(f"エラー: ファイル '{input_filename}' が見つかりません。")
        return
    
    with open(input_filename, 'r') as f:
        # ファイルの中身を全部読み込んで、空白や改行、カンマで分割してリストにする
        content = f.read().replace(',', ' ') # カンマをスペースに置換
        tokens = content.split()
        
        # 16進数変換
        v_mncore = []
        for token in tokens:
            val = hex_to_double(token)
            if val is not None:
                v_mncore.append(val)

    # データ数の確認
    count = len(v_mncore)
    print(f"データを {count} 個 読み込みました。")
    
    if count != 11:
        print(f"⚠️ 注意: データ数が {count} 個です。(想定は11個)")

    if count == 0:
        print("有効なデータがありませんでした。")
        return

    # r軸の作成
    # 11個データがあれば、i=0~10 なので 1.0 + 1.0 = 2.0 まで作られます
    r_data = np.array([r_start + i * dr for i in range(count)])

    # --- プロット処理 ---
    
    # 厳密解のカーブデータ (少し広めに描画)
    r_exact = np.linspace(0.95, 2.05, 200)
    v_exact = lj_exact(r_exact)

    plt.rcParams.update({'font.size': 18})
    plt.figure(figsize=(10, 6))
    
    # 1. 厳密解 (黒実線)
    plt.plot(r_exact, v_exact, label='Exact Solution (LJ)', color='black', linewidth=2.0, alpha=0.7)
    
    # 2. MN-Core結果 (赤丸)
    plt.scatter(r_data, v_mncore, label='MN-Core Result', color='red', s=100, zorder=5, edgecolors='black')

    # レイアウト
    plt.xlabel('Distance r', fontsize=20)
    plt.ylabel('Potential V(r)', fontsize=20)
    plt.title('Verification of LJ Potential', fontsize=18)
    
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=16, frameon=False)
    
    # 表示範囲 (データに合わせて調整)
    y_vals = v_mncore + list(v_exact)
    y_min = min(y_vals)
    y_max = max(y_vals)
    
    # 少し余裕を持たせる
    margin = (y_max - y_min) * 0.1
    plt.ylim(y_min - margin, y_max + margin)
    plt.xlim(0.9, 2.1)
    
    # 保存 (カレントディレクトリ)
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"グラフを保存しました: {output_filename}")

if __name__ == "__main__":
    main()