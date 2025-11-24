import re

def main():
    # --- 設定 ---
    input_file = 'baneljfloat.dmp'        # 単精度版のダンプファイル名
    output_file = 'baneljfloatresult.txt' # 出力ファイル名
    dt = 0.001

    data_map = {}

    print(f"'{input_file}' を読み込んでいます...")

    # 正規表現はそのまま
    pattern = re.compile(r"DEBUG-L1BM\(.*?,(\d+)\):\((.*?)\)")

    with open(input_file, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                idx = int(match.group(1))
                val_str = match.group(2) # ここが "val1, val2" になっている可能性あり
                
                try:
                    # ★修正ポイント: カンマで区切って最初の要素を使う
                    if ',' in val_str:
                        val_str = val_str.split(',')[0]
                    
                    val = float(val_str)
                    data_map[idx] = val
                except ValueError:
                    pass 

    print(f"抽出されたデータ数: {len(data_map)}")

    if len(data_map) == 0:
        print("エラー: データが抽出できませんでした。ダンプファイルの中身を確認してください。")
        return

    print(f"'{output_file}' に書き出しています...")

    with open(output_file, 'w') as out:
        # ヘッダー書き込み
        out.write("# Time\tPos\tPotentialE\tKineticE\tTotalE\n")

        max_index = max(data_map.keys())
        step = 0
        
        # 単精度でもアドレス間隔は4 (16バイト=4長語アライン) ではなく
        # ジェネレータでは「16ずつ」増やしているのでそれに合わせる
        for base_idx in range(0, max_index + 1, 16):
            if (base_idx in data_map and 
                base_idx + 4 in data_map and 
                base_idx + 8 in data_map and 
                base_idx + 12 in data_map):

                total_e = data_map[base_idx]
                pos     = data_map[base_idx + 4]
                pe      = data_map[base_idx + 8]
                ke      = data_map[base_idx + 12]
                
                time = step * dt * 10 # 10ステップ間引きなので時間は10倍進む

                out.write(f"{time:.6f}\t{pos:.6f}\t{pe:.6f}\t{ke:.6f}\t{total_e:.6f}\n")
                
                step += 1

    print("完了しました。")

if __name__ == "__main__":
    main()
