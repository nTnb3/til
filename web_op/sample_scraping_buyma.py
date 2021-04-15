import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from create_ja_area_list import prefecture

# Webページを取得して解析する
bym_url = "https://www.buyma.com/item/64033011/"
session = HTMLSession()
r = session.get(bym_url)


soup = BeautifulSoup(r.text, 'html.parser')


# スクレイピング
# カテゴリをselectorから取得
category = soup.select("#s_cate > dd > a")

# シーズンをselectorから取得
season = soup.select("#s_season > dd > a")

# テーマをselectorから取得
theme = soup.select("dt:contains(""テーマ"") ~ dd")

# タグをselectorから取得
tag = soup.select('#detail_wrap > div.detail_main > div.n_common_tabwrap.fab-design-mg--t30.fab-design-mg--b40 > div > div.js-itemcomment-disc.itemcomment-disc.itemcomment-disc--l.fab-design-mg--r20.fab-design-pg--r20 > div > ul > li')

# 発送地をselectorから取得
buying_country = soup.select("#s_buying_area > dd > img")
buying_area = soup.select("#s_buying_area > dd > a")

# 価格
price = soup.select("#abtest_display_pc")

# 画像
# src リスト
img_list = soup.select('#detail_img > div.item-thumbs > ul > li')
# img_list = soup.select('#item_mainimg_box > div > div.bx-viewport > ul > li')

srcs = []

# # 画像の拡張子が、.jpg, .png, jpeg いずれの場合も取得
# for link in img_list:
#     img = link.find('img', class_='thumbimg item_sumb_img_tabs')
#     if img.get('src').endswith('.jpg'):
#         srcs.append(img.get('src'))
#
#     elif img.get('src').endswith('.png'):
#         srcs.append(img.get('src'))
#
#     elif img.get('src').endswith('.jpeg'):
#         srcs.append(img.get('src'))
#     else:
#         print("none")
# save_path = './img/'
#
# for i, image in enumerate(srcs):
#     re = requests.get(image)
#     i += 100
#     path = save_path + f'{i}.' + image.split('.')[-1]
#     with open(path, 'wb') as f:
#         f.write(re.content)

print(" - カテゴリ:")
for e in category:
    print(e.get_text())

print("\n")

print(" - シーズン:")
for e in season:
    print(e.get_text())

print("\n")

print(" - テーマ:")
for e in theme:
    print(e.get_text())

print("\n")

print(" - タグ:")
for e in tag:
    print(e.get_text())

print("\n")

print(" - 発送国:")
for e in buying_country:
    country = e.attrs['alt']
    if country in prefecture:
        country = "日本"
    print("area:", country)

print("\n")

print(" - 発送地:")
for e in buying_area:
    print(e.get_text())

print("\n")

print(" - 価格:")
for e in price:
    p = e.get_text()[1:]
    print(p)

print("\n")



