# MN-Coreの結果を１０進数に変更し，体裁を整えたテキストファイルを出力するスクリプト
import struct
import os

def main():
    # --- ユーザー入力 ---
    print("--- MN-Core Result Parser (9-digit Precision) ---")
    try:
        interval_input = input("出力間隔（何ステップに1回出力しましたか？）を入力してください (例: 50): ")
        output_interval = int(interval_input)
    except ValueError:
        print("エラー: 整数を入力してください。")
        return

    # --- 設定 ---
    input_filename = '0205_freemd4_v=0.5~1.0.txt'
    output_filename = '0205_freemd4_v=0.5~1.0_decimal.txt'
    dt = 0.001
    1
    # 1出力フレームあたりのデータ行数構成
    # KE: 4粒子分 = 4 lines
    # PE: 4x4行列 = 16 lines (うち最後4つはinf)
    lines_per_frame = 4 + 16

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

    # --- フレーム数計算とデータ分割 ---
    total_lines = len(lines)
    n_frames = total_lines // lines_per_frame
    
    print(f"Total lines: {total_lines}")
    print(f"Detected output frames: {n_frames}")
    print(f"Total simulation steps: {n_frames * output_interval}")
    
    if total_lines % lines_per_frame != 0:
        print("⚠️ 警告: データ行数が想定（20の倍数）と一致しません。余分なデータは無視されます。")

    # データ分割位置
    split_index = n_frames * 4
    
    ke_hex_data = lines[:split_index]
    pe_hex_data = lines[split_index : split_index + (n_frames * 16)]

    # 数値変換
    print("Converting hex to float...")
    ke_vals = [hex_to_float(h) for h in ke_hex_data]
    pe_vals = [hex_to_float(h) for h in pe_hex_data]

    # --- 計算と出力 ---
    # ヘッダー作成 (桁数が増えるので幅を少し広げました: 15 -> 20)
    header = f"{'Time [s]':<12} {'Potential':<20} {'Kinetic':<20} {'Total':<20}"
    
    results = []
    
    print("Processing data...")
    for i in range(n_frames):
        # 1. 時間
        t = i * output_interval * dt
        
        # 2. 運動エネルギー
        ke_block = ke_vals[i*4 : (i+1)*4]
        ke_sum = sum(ke_block)
        
        # 3. ポテンシャルエネルギー
        pe_block_full = pe_vals[i*16 : (i+1)*16]
        pe_valid = pe_block_full[:12] 
        pe_sum = sum(pe_valid) / 2.0
        
        # 4. 全エネルギー
        total_energy = ke_sum + pe_sum
        
        # ★ここを変更: 有効数字9桁 (.9g) にし、幅を20文字確保
        # Timeも .9g にして精度を保ちます
        line_str = f"{t:<12.9g} {pe_sum:<20.9g} {ke_sum:<20.9g} {total_energy:<20.9g}"
        results.append(line_str)

    # --- ファイル保存 ---
    with open(output_filename, 'w') as f:
        f.write(header + "\n")
        f.write("-" * 75 + "\n") # 区切り線も少し長く
        for line in results:
            f.write(line + "\n")
            
    print(f"完了: 結果を '{output_filename}' に保存しました。(有効数字9桁)")

if __name__ == "__main__":
    main()