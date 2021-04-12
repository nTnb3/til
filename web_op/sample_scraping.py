import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Webページを取得して解析する
en_prod_url = "https://fr.louisvuitton.com/fra-fr/produits/sneaker-lv-trainer-nvprod2510017v#1A8KD6"
jp_prod_tmp_url = "https://jp.louisvuitton.com/jpn-jp/search/"


# セッション開始
session = HTMLSession()
r = session.get(en_prod_url)


# 外国語ページから型番をclassから取得
product_no = r.html.find('.lv-product__details-sku')
print(product_no)

# 取得した型番から日本語版ページにアクセスする
jp_prod_url = jp_prod_tmp_url + product_no[0].text

r = session.get(jp_prod_url)

# スクレイピング
# 製品名をclassから取得
product_title = r.html.find('.lv-product__title')
# 型番をclassから取得
product_no = r.html.find('.lv-product__details-sku')
# 製品仕様をidから取得
read_more = r.html.find('#read-more')
# サイズ一覧をclassから取得
size = r.html.find('.lv-product-panel-list__item-name')
# カラー一覧をclassから取得
color = r.html.find('.lv-product-card__url')

# size_table = r.html.find('td')
# size_table = r.html.find('.lv-modal')


print(" - 製品名:")
for e in product_title:
    print(e.text)

print("\n")

print(" - 型番:")
for e in product_no:
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

print(" - カラー：")
for e in color:
    print(e.text)