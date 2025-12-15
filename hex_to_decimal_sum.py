import struct
import sys

# --- 設定 ---
input_filename = 'freemd4jissenn.txt'  # ここに読み込むファイル名を指定

def hex_to_float(hex_str):
    """8桁16進数文字列を単精度浮動小数点数(float)に変換"""
    try:
        # "0x" がついていたら削除
        clean_hex = hex_str.replace("0x", "").replace(",", "").strip()
        # バイナリに変換してからfloatとして解釈 (Big Endian)
        return struct.unpack('>f', bytes.fromhex(clean_hex))[0]
    except Exception as e:
        return None

def main():
    try:
        with open(input_filename, 'r') as f:
            # 空白や改行で区切られたすべての単語をリストにする
            data_list = f.read().split()
    except FileNotFoundError:
        print(f"エラー: '{input_filename}' が見つかりません。")
        return

    print(f"{'Idx':<4} | {'Hex':<10} | {'Decimal'}")
    print("-" * 40)

    group_sum = 0.0
    group_count = 0
    total_count = 0

    for hex_str in data_list:
        val = hex_to_float(hex_str)
        
        if val is None:
            continue # 変換できない文字列はスキップ

        total_count += 1
        group_count += 1
        group_sum += val

        # 個別の値を表示
        print(f"{total_count:<4} | {hex_str:<10} | {val:.6f}")

        # 4つごとに合計を表示してリセット
        if group_count == 4:
            print("-" * 40)
            print(f"   >>> Group Sum : {group_sum:.6f}")
            print("=" * 40)
            
            group_sum = 0.0
            group_count = 0

    # もし最後に半端な余りがあれば合計を表示
    if group_count > 0:
        print("-" * 40)
        print(f"   >>> Remaining Sum : {group_sum:.6f}")
        print("=" * 40)

if __name__ == "__main__":
    main()