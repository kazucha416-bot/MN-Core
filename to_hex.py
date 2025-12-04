import struct
import sys

def float_to_hex_mixed(value):
    """
    数値をIEEE 754の倍精度(64bit)と単精度(32bit)の
    16進数文字列に変換して返します。
    """
    try:
        # 入力をfloat型にキャスト
        val_float = float(value)
        
        # --- 倍精度 (Double, 64bit) ---
        packed64 = struct.pack('>d', val_float)
        int_val64 = struct.unpack('>Q', packed64)[0]
        hex64 = f"{int_val64:016x}"

        # --- 単精度 (Float, 32bit) ---
        packed32 = struct.pack('>f', val_float)
        int_val32 = struct.unpack('>I', packed32)[0]
        hex32 = f"{int_val32:08x}"
        
        return hex64, hex32
        
    except ValueError:
        return None, None

# --- 実行ブロック ---
if __name__ == "__main__":
    print("数値を入力してください (終了するには 'q' または Ctrl+C)")
    
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() == 'q':
                break
            
            # 変換
            hex64, hex32 = float_to_hex_mixed(user_input)
            
            if hex64 is not None:
                print(f"Double (64bit): {hex64}")
                print(f"Float  (32bit): {hex32}")
            else:
                print("エラー: 数値を入力してください")
            
            print("-" * 20) # 区切り線

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"エラー: {e}")