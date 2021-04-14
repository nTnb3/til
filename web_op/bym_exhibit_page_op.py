import time

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

# Webページを取得して解析する
bym_url = "https://www.buyma.com/my/sell/new?tab=b"
# ブラウザを起動の設定(これやるとヴィトンページが上手く動作しない)
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# # ブラウザを起動する
# driver = webdriver.Chrome(options=options)

# ブラウザを起動する
driver = webdriver.Chrome()

# ブラウザでアクセスする
driver.get(bym_url)

# 以下、web操作
# ログイン
login_id = "tanabe.naoto3@gmail.com"
login_password = "n0313123"
# id入力フォームをアクティブに
login = driver.find_element_by_id('txtLoginId')
# id入力し、Enterキーを押下
login.send_keys(login_id)

# password入力フォームをアクティブに
login = driver.find_element_by_id('txtLoginPass')
# password入力し、Enterキーを押下
login.send_keys(login_password)

login_btn = driver.find_element_by_id('login_do')
login_btn.click()
time.sleep(3)


# 出品ページにて
# 画像アップロード
# img_upload = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[1]/div/div/div[2]/div/div/div[1]/div/div/div')
# img_upload.click()
# time.sleep(3)
# img_upload.send_keys("/Users/taguchinaoki/workspace/study/til/web_op/img/100.jpg")
# time.sleep(10)

# 商品名
item_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/div[1]/div/div[2]/div/div/div[1]/input')
item_name.send_keys("hogehoge")
time.sleep(10)



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






