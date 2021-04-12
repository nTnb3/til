import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Webページを取得して解析する
# url = "https://jp.louisvuitton.com/jpn-jp/products/pochette-melanie-mm-monogram-empreinte-nvprod2020033v#M68707"
url = "https://jp.louisvuitton.com/jpn-jp/products/placed-graphic-shirt-nvprod2550073v"

# セッション開始
session = HTMLSession()
r = session.get(url)


# スクレイピング
# 製品名をclassから取得
product_title = r.html.find('.lv-product__title')
# 製品仕様をidから取得
read_more = r.html.find('#read-more')
# サイズ一覧をclassから取得
size = r.html.find('.lv-product-panel-list__item-name')

# size_table = r.html.find('td')
# size_table = r.html.find('.lv-modal')


print(" - 製品名:")
for e in product_title:
    print(e.text)

print("\n")

print(" - 製品仕様：")
for e in read_more:
    print(e.text)

print("\n")

print(" - サイズ：")
for e in size:
    print(e.text)

print("\n")

# print(" - サイズリスト：")
# for e in size_table:
#     print(e.text)