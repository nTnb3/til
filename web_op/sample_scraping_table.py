import pandas as pd


# Webページを取得して解析する
# url = "https://jp.louisvuitton.com/jpn-jp/products/pochette-melanie-mm-monogram-empreinte-nvprod2020033v#M68707"
# url = "https://jp.louisvuitton.com/jpn-jp/products/placed-graphic-shirt-nvprod2550073v"
url = "https://www.buyma.com/item/52558726/"

data = pd.read_html(url, header=0)

print(data)

from requests_html import HTMLSession

# 観測データのアドレス（例：東京）
url = "https://www.oreilly.co.jp/ebook/"

# GETメソッドでリクエストを送信
session = HTMLSession()
r = session.get(url)

# ブラウザエンジンでHTMLをレンダリング
# 表の描画に若干時間がかかるためsleepで待機時間を設定
r.html.render(sleep=3)

# データを抽出
cell_data = r.html.find("td.price")
print(cell_data)
# 先頭のデータを変数に格納し空のセルを除去
output_data = []
for item in cell_data:
    print(item.text)