import struct
import sys

def hex_to_double(hex_str):
    try:
        # 入力から 0x や 空白、_ を取り除いてきれいにする
        clean_hex = hex_str.strip().lower().replace('0x', '').replace('_', '')

        # 桁数チェック (16桁 = 64bit)
        if len(clean_hex) != 16:
            return f"エラー: 入力が {len(clean_hex)} 桁です。16桁（64bit）の16進数を入力してください。"

        # 変換 (ビッグエンディアンのdoubleとして解釈)
        value = struct.unpack('!d', bytes.fromhex(clean_hex))[0]
        return value

    except ValueError:
        return "エラー: 有効な16進数の文字(0-9, a-f)のみを使ってください。"
    except Exception as e:
        return f"予期せぬエラー: {e}"

if __name__ == "__main__":
    # パターン1: コマンドライン引数がある場合 (例: python hex2dec.py 3fe...)
    if len(sys.argv) > 1:
        input_val = sys.argv[1]
        print(hex_to_double(input_val))
        
    # パターン2: 引数がない場合、対話モードで入力を待つ
    else:
        print("--- 16進数(16桁) -> double変換ツール ---")
        print("変換したい値を入力してください (例: 3fec0e4466666667)")
        print("終了するには Ctrl+C を押してください。")
        
        while True:
            try:
                # 入力を受け付ける
                user_input = input("\n入力 >> ")
                if not user_input: continue # 空エンターならスキップ
                
                result = hex_to_double(user_input)
                print(f"結果 -> {result}")
                
            except KeyboardInterrupt:
                print("\n終了します。")
                break