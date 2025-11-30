import struct
import sys

def float_to_hex64(value):
    """
    数値をIEEE 754倍精度浮動小数点数(64bit)の
    16桁16進数文字列に変換して返します。
    """
    try:
        # 入力をfloat型にキャスト
        val_float = float(value)
        
        # double(8bytes)としてパックし、unsigned long long(8bytes)としてアンパック
        packed = struct.pack('>d', val_float)
        int_val = struct.unpack('>Q', packed)[0]
        
        # 16桁の16進数文字列にフォーマット (0埋め)
        return f"{int_val:016x}"
        
    except ValueError:
        return "エラー: 数値を入力してください"

# --- 実行ブロック ---
if __name__ == "__main__":
    print("数値を入力してください (終了するには 'q' または Ctrl+C)")
    
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'q':
                break
            
            # 変換して表示
            hex_result = float_to_hex64(user_input)
            print(f"Hex (64bit): {hex_result}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"エラー: {e}")