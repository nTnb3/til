import time

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

# Webページを取得して解析する
# url = "https://jp.louisvuitton.com/jpn-jp/products/pochette-melanie-mm-monogram-empreinte-nvprod2020033v#M68707"
# jp_prod_url = "https://jp.louisvuitton.com/jpn-jp/products/placed-graphic-shirt-nvprod2550073v"
jp_prod_url ="https://jp.louisvuitton.com/jpn-jp/products/vertical-trunk-pochette-monogram-reverse-canvas-nvprod1580032v"

# ブラウザを起動の設定(これやるとヴィトンページが上手く動作しない)
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# ブラウザを起動する
# driver = webdriver.Chrome(options=options)

# ブラウザを起動する
driver = webdriver.Chrome()

# ブラウザでアクセスする
driver.get(jp_prod_url)

# 以下、web操作
# サイズガイドを取得し、クリック
is_table = True
try:
    element = driver.find_element_by_class_name('lv-product-size-guide__button').click()
except:
    is_table = False

# 文字コードをUTF-8に変換
html = driver.page_source.encode('utf-8')

# ブラウザを閉じる
driver.quit()

if is_table:
    # BeautifulSoupでhtmlをパース
    soup = BeautifulSoup(html, "html.parser")

    # table取得
    table = soup.findAll("table", {"class": "lv-size-guide-table__table"})[0]
    rows = table.findAll("tr")
    for row in rows:
        csvRow = []
        for cell in row.findAll(['td', 'th']):
            csvRow.append(cell.get_text())
        print(csvRow)

# # 型番検索用に検索フォームを取得
# x = driver.find_element_by_class_name('lv-search-input__input')
# # 型番入力し、Enterキーを押下
# x.send_keys(prod_no)
# time.sleep(10)
# x.send_keys(Keys.ENTER)
# time.sleep(10)



