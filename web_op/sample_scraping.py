import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Webページを取得して解析する
en_prod_url = "https://fr.louisvuitton.com/fra-fr/produits/pochette-melanie-mm-monogram-empreinte-nvprod2020033v"
jp_prod_tmp_url = "https://jp.louisvuitton.com/jpn-jp/search/"


# セッション開始
session = HTMLSession()
r = session.get(en_prod_url)


# 外国語ページから型番をclassから取得
product_code = r.html.find('.lv-product__details-sku')

# 取得した型番から日本語版ページにアクセスする
jp_prod_url = jp_prod_tmp_url + product_code[0].text
# jp_prod_url = "https://jp.louisvuitton.com/jpn-jp/products/lv-trainer-sneaker-nvprod2510017v"

r = session.get(jp_prod_url)
soup = BeautifulSoup(r.text, 'html.parser')

# スクレイピング
# 製品名をclassから取得
product_title = r.html.find('.lv-product__title')
# 型番をclassから取得
product_code = r.html.find('.lv-product__details-sku')
# 製品仕様をidから取得
read_more = r.html.find('#read-more')
# サイズ一覧をclassから取得
size = r.html.find('.lv-product-panel-list__item-name')




# size_table = r.html.find('td')
# size_table = r.html.find('.lv-modal')


print(" - 製品名:")
for e in product_title:
    print(e.text)
    product_name = e.text

print("\n")

print(" - 型番:")
for e in product_code:
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

# カラー一覧をclassから取得
print(" - カラー：")
is_bag = True
color_list = []
if is_bag:
    color = r.html.find('.lv-choice')
    for e in color:
        if e.text != product_name:
            color_list.append(e.text)
else:
    color = r.html.find('.lv-product-card__url')
    for e in color:
        color_list.append(e.text)
for c in color_list:
    print(c)

print("\n")

print(" - id:")
product_code_list = []
if is_bag:
    product_codes_e = r.html.find('.lv-choice')
    # lv-product-card__name list-label-m
    for e in product_codes_e:
        if e.text != product_name:
            product_code_list.append(e.attrs["id"])
else:
    product_codes_e = r.html.find('.lv-product-card__name')
    # lv-product-card__name list-label-m
    for e in product_codes_e:
        product_code_list.append(e.attrs["id"].split('-')[-1])
for code in product_code_list:
    print(code)