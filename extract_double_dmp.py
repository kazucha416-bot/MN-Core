import re

def main():
    input_file = 'baneljdouble.dmp'
    output_file = 'baneljdoubleresult.txt'
    dt = 0.01  # 時間刻み幅

    # データを格納する辞書 (index -> value)
    data_map = {}

    print(f"'{input_file}' を読み込んでいます...")

    # 正規表現: "DEBUG-L1BM(n0c0b0,12):(-0.657017)..." から インデックスと値を抽出
    # 値は (...) の中にある
    pattern = re.compile(r"DEBUG-L1BM\(.*?,(\d+)\):\((.*?)\)")

    with open(input_file, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                idx = int(match.group(1))
                val_str = match.group(2)
                try:
                    val = float(val_str)
                    data_map[idx] = val
                except ValueError:
                    pass # 数値に変換できない場合はスキップ

    print(f"抽出されたデータ数: {len(data_map)}")
    print(f"'{output_file}' に書き出しています...")

    with open(output_file, 'w') as out:
        # ヘッダー書き込み
        out.write("# Time\tPos\tPotentialE\tKineticE\tTotalE\n")

        # 1ステップあたり16インデックス進む (0, 4, 8, 12)
        # 最大インデックスまでスキャン
        max_index = max(data_map.keys())
        step = 0
        
        for base_idx in range(0, max_index + 1, 16):
            # 必要なデータが揃っているか確認
            if (base_idx in data_map and 
                base_idx + 4 in data_map and 
                base_idx + 8 in data_map and 
                base_idx + 12 in data_map):

                total_e = data_map[base_idx]
                pos     = data_map[base_idx + 4]
                pe      = data_map[base_idx + 8]
                ke      = data_map[base_idx + 12]
                
                time = step * dt

                # フォーマットして書き込み
                out.write(f"{time:.6f}\t{pos:.6f}\t{pe:.6f}\t{ke:.6f}\t{total_e:.6f}\n")
                
                step += 1

    print("完了しました。")

if __name__ == "__main__":
    main()
