import struct
import os

def main():
    # --- 設定 ---
    input_filename = 'freemd4result.txt'
    output_filename = '1228_energy_log.txt'
    dt = 0.001
    
    # 1ステップあたりのデータ行数構成
    # KE: 4粒子分 = 4 lines
    # PE: 4x4行列 = 16 lines (うち最後4つはinf)
    lines_per_step = 4 + 16

    # --- 関数定義 ---
    def hex_to_float(hex_str):
        s = hex_str.strip().replace('0x', '').replace(',', '')
        if len(s) > 8: s = s[:8]
        s = s.zfill(8)
        try:
            return struct.unpack('>f', bytes.fromhex(s))[0]
        except ValueError:
            return 0.0

    # --- データ読み込み ---
    if not os.path.exists(input_filename):
        print(f"エラー: ファイル '{input_filename}' が見つかりません。")
        return

    print(f"Reading from: {input_filename}")
    
    with open(input_filename, 'r') as f:
        # 空行を除去してリスト化
        lines = [l.strip() for l in f if l.strip()]

    # --- ステップ数計算とデータ分割 ---
    total_lines = len(lines)
    n_steps = total_lines // lines_per_step
    
    print(f"Total lines: {total_lines}")
    print(f"Detected steps: {n_steps}")
    
    if total_lines % lines_per_step != 0:
        print("⚠️ 警告: データ行数が想定（20の倍数）と一致しません。余分なデータは無視されます。")

    # データ分割位置
    # ファイルの前半: 全ステップのKE (Steps * 4)
    # ファイルの後半: 全ステップのPE (Steps * 16)
    split_index = n_steps * 4
    
    ke_hex_data = lines[:split_index]
    pe_hex_data = lines[split_index : split_index + (n_steps * 16)]

    # 数値変換
    ke_vals = [hex_to_float(h) for h in ke_hex_data]
    pe_vals = [hex_to_float(h) for h in pe_hex_data]

    # --- 計算と出力 ---
    # ヘッダー作成
    header = f"{'Time [s]':<10} {'Potential':<15} {'Kinetic':<15} {'Total':<15}"
    print("\n" + header)
    print("-" * 60)

    results = []
    
    for i in range(n_steps):
        # 1. 時間
        t = i * dt
        
        # 2. 運動エネルギー (4つの合計)
        ke_block = ke_vals[i*4 : (i+1)*4]
        ke_sum = sum(ke_block)
        
        # 3. ポテンシャルエネルギー (16個のブロックのうち、先頭12個を合計して半分にする)
        pe_block_full = pe_vals[i*16 : (i+1)*16]
        # 最後4つのinf(7f800000)を無視するため先頭12個を取得
        pe_valid = pe_block_full[:12] 
        pe_sum = sum(pe_valid) / 2.0
        
        # 4. 全エネルギー
        total_energy = ke_sum + pe_sum
        
        # 文字列整形
        line_str = f"{t:<10.3f} {pe_sum:<15.6f} {ke_sum:<15.6f} {total_energy:<15.6f}"
        results.append(line_str)
        print(line_str)

    # --- ファイル保存 ---
    with open(output_filename, 'w') as f:
        f.write(header + "\n")
        f.write("-" * 60 + "\n")
        for line in results:
            f.write(line + "\n")
            
    print(f"\nSaved results to: {output_filename}")

if __name__ == "__main__":
    main()