import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Webページを取得して解析する
url = "https://jp.louisvuitton.com/jpn-jp/products/pochette-melanie-mm-monogram-empreinte-nvprod2020033v#M68707"

# セッション開始
session = HTMLSession()
r = session.get(url)

# スクレイピング(製品名の取得)
product_title = r.html.find('.lv-product__title')
read_more = r.html.find('#read-more')
# read-more = r.html.find('#read-more > p ')

print(" - 製品名:")
for e in product_title:
    print(e.text)

print("\n")

print(" - 製品仕様：")
for e in read_more:
    print(e.text)