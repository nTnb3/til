import time

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

# Webページを取得して解析する
# bym_url = "https://www.buyma.com/item/66263260/?ba_af=recommend_at_itemdetail"
bym_url = "https://www.buyma.com/item/64033011/"
# ブラウザを起動の設定(これやるとヴィトンページが上手く動作しない)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
# ブラウザを起動する
driver = webdriver.Chrome(options=options)

# ブラウザを起動する
# driver = webdriver.Chrome()

# ブラウザでアクセスする
driver.get(bym_url)

# 以下、web操作
small_img_sel_path = '#detail_img > div.item-thumbs > ul > li'
elements = driver.find_element_by_css_selector(small_img_sel_path)
# 文字コードをUTF-8に変換
html = driver.page_source.encode('utf-8')

# BeautifulSoupでhtmlをパース
soup = BeautifulSoup(html, "html.parser")

img_list = soup.select('#item_mainimg_box > div > div.bx-viewport > ul > li')

srcs = []

# 画像の拡張子が、.jpg, .png, jpeg いずれの場合も取得
for link in img_list:
    img = link.find('img', class_='item-main-image')
    if img.get('src').endswith('.jpg'):
        srcs.append(img.get('src'))

    elif img.get('src').endswith('.png'):
        srcs.append(img.get('src'))

    elif img.get('src').endswith('.jpeg'):
        srcs.append(img.get('src'))
    else:
        print("none")
save_path = './img/'

for i, image in enumerate(srcs):
    re = requests.get(image)
    i += 100
    path = save_path + f'{i}.' + image.split('.')[-1]
    with open(path, 'wb') as f:
        f.write(re.content)








# サイズガイドを取得し、クリック
is_color = True
try:
    element = driver.find_element_by_css_selector('#colorsize > div.colorsize_select.js-color-select').click()
except:
    is_table = False

# 文字コードをUTF-8に変換
html = driver.page_source.encode('utf-8')

# ブラウザを閉じる
driver.quit()

# BeautifulSoupでhtmlをパース
soup = BeautifulSoup(html, "html.parser")

# カラーをselectorから取得
# color = soup.select("#colorsize > div.colorsize_select.js-color-select > ul > li")
color = soup.select("#colorsize > div.colorsize_select.js-color-select > ul > li > span")
color_num = len(color)/2
print(" - カラー:")
count = 0
for e in color:
    if count%2 == 0:
        extract_color = e.attrs
        color_label = list(extract_color.values())[0][1]
        print("color_label:", color_label)
    else:
        c = e.get_text()
        print("color:", c)
    count += 1

print("\n")






