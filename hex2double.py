import struct
import sys

def hex_to_number(hex_str):
    try:
        # 入力から 0x や 空白、_ を取り除いてきれいにする
        clean_hex = hex_str.strip().lower().replace('0x', '').replace('_', '')

        # --- 桁数による分岐 ---
        length = len(clean_hex)

        if length == 8:
            # 単精度 (32bit float)
            # '!f' はビッグエンディアンのfloat
            value = struct.unpack('!f', bytes.fromhex(clean_hex))[0]
            return f"Float (32bit) : {value}"

        elif length == 16:
            # 倍精度 (64bit double)
            # '!d' はビッグエンディアンのdouble
            value = struct.unpack('!d', bytes.fromhex(clean_hex))[0]
            return f"Double(64bit) : {value}"

        else:
            return f"エラー: 入力が {length} 桁です。\n" \
                   f"  - 単精度(float) の場合は 8桁\n" \
                   f"  - 倍精度(double)の場合は 16桁\n" \
                   f"  の16進数を入力してください。"

    except ValueError:
        return "エラー: 有効な16進数の文字(0-9, a-f)のみを使ってください。"
    except Exception as e:
        return f"予期せぬエラー: {e}"

if __name__ == "__main__":
    print("--- 16進数 -> 浮動小数点数 変換ツール ---")
    print("  * 8桁  -> float (単精度) として変換")
    print("  * 16桁 -> double(倍精度) として変換")

    # パターン1: コマンドライン引数がある場合
    if len(sys.argv) > 1:
        input_val = sys.argv[1]
        print(hex_to_number(input_val))
        
    # パターン2: 引数がない場合、対話モード
    else:
        print("変換したい値を入力してください (例: 3f800000 または 3ff0000000000000)")
        print("終了するには Ctrl+C を押してください。")
        
        while True:
            try:
                # 入力を受け付ける
                user_input = input("\n入力 >> ")
                if not user_input: continue # 空エンターならスキップ
                
                result = hex_to_number(user_input)
                print(f"結果 -> {result}")
                
            except KeyboardInterrupt:
                print("\n終了します。")
                break