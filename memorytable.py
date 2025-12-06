import matplotlib.pyplot as plt

# プレゼン用のフォント設定
plt.rcParams.update({'font.size': 14, 'font.family': 'sans-serif'})

def draw_memory_table():
    # 1. データ定義
    # カラム名 (ヘッダー)
    col_labels = ['0', '2', '4', '6', '8']
    # 行名 (左端)
    row_labels = ['lm', 'ln', 'lr', 'ls']
    
    # テーブルの中身 (空文字 '' は空白セル)
    # LaTeX記法 ($...$) を使って数式やギリシャ文字をきれいに表示
    cell_text = [
        ['$x$', '$dt$', '$m$', '$\epsilon$', '$\sigma$'],  # lm行
        ['$v_0$', '', '', '', ''],                          # ln行
        ['ce06', 'ce12', '', '', ''],                       # lr行
        ['cf06', 'cf12', '', '', '']                        # ls行
    ]

    # 2. 図の準備
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_axis_off() # 軸は消す

    # 3. テーブルの作成
    # colWidthsで列の幅を調整
    table = ax.table(
        cellText=cell_text,
        colLabels=col_labels,
        rowLabels=row_labels,
        loc='center',
        cellLoc='center',
        colWidths=[0.15] * 5  # 各列の幅を等しく設定
    )

    # 4. スタイリング（かっこよくする部分）
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1, 2.5) # 縦方向の高さを広げて見やすく (横, 縦)

    # セルごとのスタイル設定
    # (row_index, col_index) でアクセス。ヘッダーは row=0, 行ラベルは col=-1
    
    cells = table.get_celld()
    
    # 色の設定
    header_color = '#34495e' # 濃いブルーグレー (ヘッダー用)
    row_label_color = '#34495e'
    cell_bg_color = '#ecf0f1' # 薄いグレー (データセル用)
    text_color_header = 'white'
    text_color_cell = 'black'
    edge_color = 'white' # 枠線の色

    for (row, col), cell in cells.items():
        cell.set_linewidth(1.5)      # 枠線の太さ
        cell.set_edgecolor(edge_color) # 枠線の色

        # ヘッダー行 (row == 0)
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color=text_color_header, fontweight='bold')
        
        # 行ラベル (col == -1)
        elif col == -1:
            cell.set_facecolor(row_label_color)
            cell.set_text_props(color=text_color_header, fontweight='bold')
        
        # データセル
        else:
            cell.set_facecolor(cell_bg_color)
            cell.set_text_props(color=text_color_cell)
            
            # データが入っているセルだけ少しフォントを大きくするなどの調整も可能
            if cell_text[row-1][col]: # データがある場合
                 cell.set_text_props(weight='medium')

    # タイトル
    plt.title('MN-Core Memory Map Layout', fontsize=18, pad=20, color='#2c3e50', fontweight='bold')

    # 保存
    plt.tight_layout()
    plt.savefig('memory_table.png', dpi=300, bbox_inches='tight', transparent=True)
    print("保存完了: memory_table.png")
    plt.show()

if __name__ == "__main__":
    draw_memory_table()