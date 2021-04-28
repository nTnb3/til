import datetime
import time

import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import chromedriver_binary
import pywinauto
from selenium.webdriver.common.action_chains import ActionChains

CATEGORY_INDEX = 0
SEASON_ID = 1
THEME_ID = 2
COLOR_ID = 3

# Webページを取得して解析する
bym_url = "https://www.buyma.com/my/sell/new?tab=b"
# # ブラウザを起動の設定(これやるとヴィトンページが上手く動作しない)
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# # ブラウザを起動する
# driver = webdriver.Chrome(options=options)

# ブラウザを起動する
driver = webdriver.Chrome()
driver.maximize_window()
zoom_rate = "50%"
# driver.execute_script("document.body.style.zoom=\"90%\"")
driver.execute_script("document.body.style.zoom='50%'")

# ブラウザでアクセスする
driver.get(bym_url)

# 以下、web操作
# ログイン
login_id = ""
login_password = ""
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


img_upload = driver.find_element_by_xpath(
    '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[1]/div/div/div[2]/div/div/div[1]/div/div/div')
img_upload.click()
# 開くダイアログを探して接続する
# ダイアログタイトルを手掛かりにwindowを探す
findWindow = lambda: pywinauto.findwindows.find_windows(title=u'開く')[0]

# 上記Wndowを探す処理が完了したかチェックする
# pywinauto.timings.wait_until(タイムアウトまでの時間, 繰り返す間隔(Sec), 組み込み関数)
dialog = pywinauto.timings.wait_until_passes(5, 1, findWindow)

# pywinauto に探し出したダイアログを接続
pwa_app = pywinauto.Application()
pwa_app.connect(handle=dialog)
window = pwa_app[u"開く"]

addres = window.children()[39]
addres.click()

dialog_dir = window.children()[43]
photo_folder = ""

dialog_dir.type_keys(photo_folder+'{ENTER}',with_spaces=True)

# テキストボックス(ファイル名)にPATHを入力
tb = window[u"ファイル名(&N):"]
if tb.is_enabled():
    tb.click()
    edit = window.Edit4
    edit.set_focus()
    img_list = ["100.jpg", "101.jpg", "102.jpg"]
    for file_path_str in img_list:
        # ファイルを選択し、Alt + Oを押下
        edit.type_keys('{VK_LCONTROL}'+ "\"" + file_path_str + "\"", with_spaces=True)
    edit.type_keys('%O', with_spaces=True)

time.sleep(10)

# 商品名
# item_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/div[1]/div/div[2]/div/div/div[1]/input')
# item_name.send_keys("hogehoge")
# time.sleep(1)

# 商品コメント
# item_comm = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/div[2]/div/div[2]/div/div/div[1]/textarea')
# item_comm.send_keys("hogehoge")
# time.sleep(1)

# カテゴリ
# 入力部分まで移動
driver.execute_script("window.scrollTo(0, 1000);")

# spanの中にある、「選択してください」って書いてあるdivパスを取得
category1 = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/span[1]/div[1]')

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(category1)
actions.click()
actions.perform()
time.sleep(2)

category1_choice = "メンズファッション"
category1_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

for div_tag in category1_element:
    if div_tag.text == category1_choice:
        print(div_tag)
        # その国を選択する
        div_tag.click()
        break


category2 = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div[1]/span[1]/div[1]')
# time.sleep(2)

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(category2)
actions.click()
actions.perform()
time.sleep(1)

category2_choice = "ボトムス"
category2_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

for div_tag in category2_element:
    if div_tag.text == category2_choice:
        print(div_tag)
        # その国を選択する
        div_tag.click()
        break

category3 = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/div/div/div[3]/div/div[1]/span[1]/div[1]')
# time.sleep(2)

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(category3)
actions.click()
actions.perform()
time.sleep(1)

category3_choice = "パンツ"
category3_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

for div_tag in category3_element:
    if div_tag.text == category3_choice:
        print(div_tag)
        # その国を選択する
        div_tag.click()
        break



# ブランド名
brand_name = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/input')
brand_name.send_keys("Louis Vuitton")
time.sleep(1)

brand_choice = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div/p')

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(brand_choice)
actions.click()
actions.perform()
time.sleep(1)


# シーズン
# 入力部分まで移動
driver.execute_script("window.scrollTo(1000, 1500);")
# spanの中にある、「選択してください」って書いてあるdivパスを取得
season = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[4]/div/div[2]/div/div/div/div/div/span[1]/div[1]")

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(season)
actions.click()
actions.perform()
time.sleep(1)

season_choice = "2014 SS"
season_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

for div_tag in season_element:
    if div_tag.text == season_choice:
        # その国を選択する
        div_tag.click()
        break

# テーマ
# 入力部分まで移動
driver.execute_script("window.scrollTo(1500, 2000);")
# spanの中にある、「選択してください」って書いてあるdivパスを取得
theme = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[5]/div/div[2]/div/div/div/div/div/div/div/span[1]/div[1]")

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(theme)
actions.click()
actions.perform()
time.sleep(1)

theme_choice = "円高還元セール特集！"
theme_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

for div_tag in theme_element:
    if theme_choice in div_tag.text:
        div_tag.click()
        break

# タグ
tag_list_btn = driver.find_elements_by_class_name('bmm-c-ico-list-search')[1]
tag_list_btn.click()
# tag一覧を取得
tag_list_element = driver.find_elements_by_class_name("bmm-c-checkbox--tag")

check_tag_list = ["無地", "ユニセックス", "ロゴ"]
check_tag_len = len(check_tag_list)
tag_count = 0
for div_tag in tag_list_element:
    if div_tag.text in check_tag_list:
        # その国を選択する
        div_tag.click()
        tag_count += 1
        if tag_count == check_tag_len:
            break

next_btn = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[2]/div[7]/div/div/div[3]/button[2]')
next_btn.click()


# カラー
# 入力部分まで移動
driver.execute_script("window.scrollTo(2000, 2300);")
# spanの中にある、「選択してください」って書いてあるdivパスを取得
color = driver.find_element_by_class_name("sell-color-option")


# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(color)
actions.click()
actions.perform()
time.sleep(1)

color_num = 0
dict = {"ゴールド（金色）系":"金", "ブラック（黒）系":"ブラック", "グレー（灰色）系":"グレー"}
color_len = len(dict.keys())
scroll_start = 2300
for color_cate, color_detail in dict.items():
    color_num += 1
    color_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in color_element:
        if div_tag.text == color_cate:
            # その国を選択する
            div_tag.click()
            break

    color_name_path = "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[" + str(color_num) + "]/td[3]/div/div/input"
    color_name = driver.find_element_by_xpath(color_name_path)
    color_name.send_keys(color_detail)

    if color_num < color_len:
        # 入力部分まで移動
        scroll_goal = scroll_start + 50
        js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
        driver.execute_script(js_command)
        add_color_btn = driver.find_element_by_class_name('bmm-c-ico-plus')
        add_color_btn.click()
        scroll_start = scroll_goal


# サイズ
size_tab = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/ul/li[2]")
size_tab.click()

# spanの中にある、「選択してください」って書いてあるdivパスを取得
size_val = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/span[1]/div[1]")

# プルダウンをクリックし選択肢一覧を表示させる
actions = ActionChains(driver)
actions.move_to_element(size_val)
actions.click()
actions.perform()
time.sleep(1)

size_dict = {"10":"XS以下", "20":"XS以下"}
size_dict = {}
size_len = len(size_dict.keys())
if size_len > 0:
    size_val_choice = "バリエーションあり"
else:
    size_val_choice = "バリエーションなし"
size_val_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

for div_tag in size_val_element:
    if size_val_choice == div_tag.text:
        div_tag.click()
        break


if size_val_choice == "バリエーションあり":
    size_num = 0
    scroll_start = 2300
    for size, ref_size in size_dict.items():
        size_num += 1
        size_path = "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/table/tbody/tr[" + str(size_num) + "]/td[2]/div/div/div/input"
        size_name = driver.find_element_by_xpath(size_path)
        size_name.send_keys(size)

        # spanの中にある、「選択してください」って書いてあるdivパスを取得
        size_val = driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/table/tbody/tr[" + str(size_num) + "]/td[3]/div/div/span[1]/div[1]")

        # プルダウンをクリックし選択肢一覧を表示させる
        actions = ActionChains(driver)
        actions.move_to_element(size_val)
        actions.click()
        actions.perform()
        time.sleep(1)

        size_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

        for div_tag in size_element:
            if div_tag.text == ref_size:
                div_tag.click()
                break

        if size_num < size_len:
            # 入力部分まで移動
            scroll_goal = scroll_start + 100
            js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
            driver.execute_script(js_command)
            add_size_btn = driver.find_element_by_class_name('bmm-c-ico-plus')
            add_size_btn.click()
            scroll_start = scroll_goal

# 購入可能数
item_num = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input')
# id入力し、Enterキーを押下
item_num.send_keys("2")



# 型番
color_num = 0
prod_no_list = ["12DS2", "12DS3"]
prod_no_len = len(prod_no_list)
prod_no_num= 0
for prod_no in prod_no_list:
    prod_no_num += 1

    prod_no_box_path = "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[3]/div/div[2]/div/div/div[2]/table/tbody/tr[" + str(prod_no_num) + "]/td[1]/input"
    prod_no_box = driver.find_element_by_xpath(prod_no_box_path)
    prod_no_box.send_keys(prod_no)

    loc = prod_no_box.location
    scroll_start = loc["y"]
    if prod_no_num < prod_no_len:
        # 入力部分まで移動
        scroll_goal = scroll_start + 10
        js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
        driver.execute_script(js_command)
        add_prod_no_btn = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[3]/div/div[2]/div/div/div[3]/a/i')
        add_prod_no_btn.click()

time.sleep(2)

# 配送方法
# 選択部分まで移動
scroll_start = scroll_goal
scroll_goal = scroll_start + 800
js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
driver.execute_script(js_command)
time.sleep(1)

delivery_area_list = ["北海道", "北海道"]
# delivery_area_list = ["ヨーロッパ", "フランス"]
delivery_area = delivery_area_list[1]
if delivery_area == "北海道":
    del_method_btn = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[6]/div/div/div[2]/div/div/div[2]/div[1]/table/tbody/tr[12]/td[2]')
else:
    del_method_btn = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[6]/div/div/div[2]/div/div/div[2]/div[1]/table/tbody/tr[9]/td[2]')

# 配送方法をクリック
actions = ActionChains(driver)
actions.move_to_element(del_method_btn)
actions.click()
actions.perform()


# 購入期限
dead_line_element = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div/input")
dead_line = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y/%m/%d')
# 一度デフォルト入力を削除
dead_line_element.click()
text = dead_line_element.get_attribute("value")
dead_line_element.send_keys(Keys.BACKSPACE * len(text))

time.sleep(1)
dead_line_element.send_keys(dead_line)

time.sleep(1)




# 買い付け地
# 購入期限カレンダーで隠れてるので、いったん適当なところをクリック
actions = ActionChains(driver)
actions.move_to_element(dead_line_element)
actions.move_to_element_with_offset(dead_line_element, 600, 0)
actions.click()
actions.perform()
time.sleep(1)

if delivery_area == "北海道":
    # 国内をチェック
    buy_area_btn = driver.find_element_by_xpath(
        "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[1]/div/label[1]/span")
    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(buy_area_btn)
    actions.click()
    actions.perform()

    time.sleep(1)
    # 都道府県を選択するためにプルダウン部分を取得
    area_category = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[2]/div/div/div/div/span[1]/div[1]')

    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(area_category)
    actions.click()
    actions.perform()
    time.sleep(1)

    area_category_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in area_category_element:
        if div_tag.text == delivery_area:
            print(div_tag)
            # その国を選択する
            div_tag.click()
            break

else:
    buy_area_btn = driver.find_element_by_xpath(
        "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[1]/div/label[2]/span")
    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(buy_area_btn)
    actions.click()
    actions.perform()
    time.sleep(1)

    # 州を選択するためにプルダウン部分を取得
    area_category1 = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/span[1]/div[1]')

    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(area_category1)
    actions.click()
    actions.perform()
    time.sleep(1)

    area_category_element1 = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in area_category_element1:
        if div_tag.text == delivery_area_list[0]:
            print(div_tag)
            # その州を選択する
            div_tag.click()
            break

    area_category2 = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/span[1]/div[1]')
    # time.sleep(2)

    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(area_category2)
    actions.click()
    actions.perform()
    time.sleep(1)

    area_category_element2 = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in area_category_element2:
        if div_tag.text == delivery_area_list[1]:
            print(div_tag)
            # その国を選択する
            div_tag.click()
            break

# 買い付け先ショップ名
shop_element = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[3]/div/div[2]/div/div/div/div/div[1]/input")
shop_element.send_keys("Louis Vuitton 正規店")


# 発送地
loc = shop_element.location
scroll_start = loc["y"]
scroll_goal = scroll_start + 30
js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
driver.execute_script(js_command)
time.sleep(1)

if delivery_area == "北海道":
    # 国内をチェック
    send_area_btn = driver.find_element_by_xpath(
        "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[1]/div/label[1]/span")
    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(send_area_btn)
    actions.click()
    actions.perform()

    time.sleep(1)
    # 都道府県を選択するためにプルダウン部分を取得
    area_category = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[2]/div/div/div/div/span[1]/div[1]')

    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(area_category)
    actions.click()
    actions.perform()
    time.sleep(1)

    area_category_element = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in area_category_element:
        if div_tag.text == delivery_area:
            print(div_tag)
            # その国を選択する
            div_tag.click()
            break

else:
    send_area_btn = driver.find_element_by_xpath(
        "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[1]/div/label[2]/span")
    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(send_area_btn)
    actions.click()
    actions.perform()
    time.sleep(1)

    # 州を選択するためにプルダウン部分を取得
    area_category1 = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[2]/div/div[1]/div/div/span[1]/div[1]')

    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(area_category1)
    actions.click()
    actions.perform()
    time.sleep(1)

    area_category_element1 = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in area_category_element1:
        if div_tag.text == delivery_area_list[0]:
            print(div_tag)
            # その州を選択する
            div_tag.click()
            break

    area_category2 = driver.find_element_by_xpath(
        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[2]/div/div[2]/div/div/span[1]/div[1]')
    # time.sleep(2)

    # プルダウンをクリックし選択肢一覧を表示させる
    actions = ActionChains(driver)
    actions.move_to_element(area_category2)
    actions.click()
    actions.perform()
    time.sleep(1)

    area_category_element2 = driver.execute_script('return document.getElementsByClassName("Select-option")')

    for div_tag in area_category_element2:
        if div_tag.text == delivery_area_list[1]:
            print(div_tag)
            # その国を選択する
            div_tag.click()
            break

# 値段
price = "5000"
price_element = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[8]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div/input")
price_element.send_keys(price)

# メモ
# loc = price_element.location
# scroll_start = loc["y"]
# scroll_goal = scroll_start + 100
# js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
# driver.execute_script(js_command)
# time.sleep(1)
message = datetime.date.today().strftime('%Y/%m/%d') + " タグチ"
message_element = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[9]/div[1]/div/div[2]/div/div[1]/textarea")
message_element.send_keys(message)

# 下書き完了ボタン
comp_btn_element = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[10]/div/button[1]")
comp_btn_element.click()

# ブラウザを閉じる
driver.quit()







