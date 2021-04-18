import datetime
import glob
import os
import time

import chromedriver_binary
import pywinauto
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from string import Template

from bym_page_data_collector import BymPageDataCollector
from color_correspondence import color_correspondence_dict
from lv_page_data_collector import LvPageDataCollector
from create_ja_area_list import prefecture_ja, prefecture_ep
from prod_comment_template import comment
from util import merge_dict, resize_img

class BymExhibitionPageCreater(object):
    def __init__(self,
                 ref_bym_url,
                 lv_url,
                 exhbt_no,
                 exhibition_url="https://www.buyma.com/my/sell/new?tab=b",
                 login_id="tanabe.naoto3@gmail.com",
                 login_pass="n0313123",
                 title_msg="【大人気】",
                 country="",
                 img_save_root_path="C:\\Users\\ntagu\\workspace\\til\\web_op\\exhibition_page_create_bym\\img\\"):
        self.exhbit_no = exhbt_no
        self.login_id = login_id
        self.login_pass = login_pass
        self.title_msg = title_msg
        self.maker_name = "ルイヴィトン"
        self.scroll_start = 0
        self.scroll_goal = 1000

        dt_now = datetime.datetime.now()
        today = dt_now.strftime('%m-%d')
        self.bym_data_collector = BymPageDataCollector(ref_bym_url, today, exhbt_no, img_save_root_path)
        self.lv_data_collector = LvPageDataCollector(lv_url)

        self.bym_extract_data = self.bym_data_collector.data_dict
        self.lv_extract_data = self.lv_data_collector.data_dict

        if self.title_msg == "":
            self.title_msg = "【大人気】"
        if country != "":
            self.bym_extract_data["palace"][0] = country

        if self.bym_extract_data["is_enable"] and self.lv_extract_data["is_enable"]:
            self._activate_browser(exhibition_url)
            self.create_exhibit_page()
            # self._close_browser()

    def _activate_browser(self, exhibition_url, zoom_rate="60"):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        # ブラウザでアクセスする
        self.driver.get(exhibition_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()

    def create_exhibit_page(self):
        self._login_bympage()
        self._upload_img()
        self._write_prod_name()
        self._write_prod_comment()
        self._write_category()
        self._write_brand()
        self._write_season()
        self._write_theme()
        self._write_tag()
        self._write_color()
        self._write_size()
        self._write_prod_num()
        self._write_prod_code()
        self._write_delivery_method()
        self._write_buy_dead_line()
        self._write_buy_area()
        self._write_shop()
        self._write_send_area()
        self._write_price()
        self._write_memo()
        self._comp_btn()

    def _login_bympage(self):
        # id入力フォームをアクティブに
        login = self.driver.find_element_by_id('txtLoginId')
        # id入力し、Enterキーを押下
        login.send_keys(self.login_id)
        # password入力フォームをアクティブに
        login = self.driver.find_element_by_id('txtLoginPass')
        # password入力し、Enterキーを押下
        login.send_keys(self.login_pass)
        login_btn = self.driver.find_element_by_id('login_do')
        login_btn.click()
        time.sleep(3)

    def _scroll_display(self, element, y, sleeptime=1):
        loc = element.location
        scroll_start = loc["y"]
        scroll_goal = scroll_start + y
        js_command = "window.scrollTo(" + str(scroll_start) + ", " + str(scroll_goal) + ");"
        self.driver.execute_script(js_command)
        time.sleep(sleeptime)

    def _upload_img(self):
        img_upload = self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[1]/div/div/div[2]/div/div/div[1]/div/div/div')
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

        dialog_dir.type_keys(self.bym_extract_data["img_path"]+'{ENTER}',with_spaces=True)

        # テキストボックス(ファイル名)にPATHを入力
        tb = window[u"ファイル名(&N):"]
        img_path_list = glob.glob(self.bym_extract_data["img_path"] + "*")
        img_list = []
        for img_path in img_path_list:
            img_list.append(os.path.split(img_path)[1])
            #画像のリサイズ
            resize_img(img_path=img_path, img_size_tpl=(700, 700))
        if tb.is_enabled():
            tb.click()
            edit = window.Edit4
            edit.set_focus()
            img_num = 0
            if len(img_list) > 20:
                img_list = img_list[:19]
            img_len = len(img_list)
            for img_name in img_list:
                img_num += 1
                if img_num >= img_len:
                    time.sleep(2)
                    # ファイルを選択し、Alt + Oを押下
                    edit.type_keys('{VK_LCONTROL}' + "\"" + img_name + "\"" + '%O', with_spaces=True)
                else:
                    # ファイルを選択し、Alt + Oを押下
                    edit.type_keys('{VK_LCONTROL}' + "\"" + img_name + "\"", with_spaces=True)
            time.sleep(3)

    def _write_prod_name(self):
        prod_name_element = self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/div[1]/div/div[2]/div/div/div[1]/input')
        prod_name = self.maker_name + self.title_msg + self.lv_extract_data["prod_name"]
        prod_name_element.send_keys(prod_name)
        self._scroll_display(prod_name_element, 50)

    def _write_prod_comment(self):
        inserted_comment = ""
        for s in comment:
            if ("prod_spec" in s) or ("size_table" in s):
                t = Template(s)
                if len(self.lv_extract_data["size_table"]) > 0:
                    size_table = self.lv_extract_data["size_table"][0]
                else:
                    size_table = ""
                s = t.substitute(prod_spec=self.lv_extract_data["prod_spec"], size_table=size_table)
            inserted_comment += s
        prod_comm = self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[2]/div[2]/div/div[2]/div/div/div[1]/textarea')
        prod_comm.send_keys(inserted_comment)
        self._scroll_display(prod_comm, 100)

    def _write_category(self):
        # spanの中にある、「選択してください」って書いてあるdivパスを取得
        category1 = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/div/div/div[1]/div/div/span[1]/div[1]')

        # プルダウンをクリックし選択肢一覧を表示させる
        actions = ActionChains(self.driver)
        actions.move_to_element(category1)
        actions.click()
        actions.perform()
        time.sleep(2)

        category1_choice = self.bym_extract_data["category"][0]
        category1_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

        for div_tag in category1_element:
            if div_tag.text == category1_choice:
                # そのカテゴリを選択する
                div_tag.click()
                break

        category2 = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/span[1]/div[1]')
        # time.sleep(2)

        # プルダウンをクリックし選択肢一覧を表示させる
        actions = ActionChains(self.driver)
        actions.move_to_element(category2)
        actions.click()
        actions.perform()
        time.sleep(1)

        category2_choice = self.bym_extract_data["category"][1]
        category2_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

        for div_tag in category2_element:
            if div_tag.text == category2_choice:
                # そのカテゴリを選択する
                div_tag.click()
                break

        category3 = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[1]/div/div[2]/div/div/div/div/div[3]/div/div/span[1]/div[1]')
        # time.sleep(2)

        # プルダウンをクリックし選択肢一覧を表示させる
        actions = ActionChains(self.driver)
        actions.move_to_element(category3)
        actions.click()
        actions.perform()
        time.sleep(1)

        category3_choice = self.bym_extract_data["category"][2]
        category3_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

        for div_tag in category3_element:
            if div_tag.text == category3_choice:
                # そのカテゴリを選択する
                div_tag.click()
                break

    def _write_brand(self):
        # 入力部分まで移動
        self.scroll_start = self.scroll_goal
        self.scroll_goal = self.scroll_start + 300
        js_command = "window.scrollTo(" + str(self.scroll_start) + ", " + str(self.scroll_goal) + ");"
        self.driver.execute_script(js_command)
        time.sleep(1)

        brand_name = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div/input')
        brand_name.send_keys("Louis Vuitton")
        time.sleep(1)

        brand_choice = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div/p')

        # プルダウンをクリックし選択肢一覧を表示させる
        actions = ActionChains(self.driver)
        actions.move_to_element(brand_choice)
        actions.click()
        actions.perform()
        self._scroll_display(brand_name, 200)

    def _write_season(self):
        if len(self.bym_extract_data["season"]) > 0:
            # spanの中にある、「選択してください」って書いてあるdivパスを取得
            season = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[4]/div/div[2]/div/div/div/div/div/span[1]/div[1]")
            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(season)
            actions.click()
            actions.perform()
            time.sleep(1)

            season_choice = self.bym_extract_data["season"][0]
            season_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in season_element:
                if div_tag.text == season_choice:
                    # その国を選択する
                    div_tag.click()
                    break

    def _write_theme(self):
        if len(self.bym_extract_data["theme"]) > 0:
            # spanの中にある、「選択してください」って書いてあるdivパスを取得
            theme = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[5]/div/div[2]/div/div/div/div/div/div/div/span[1]/div[1]")
            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(theme)
            actions.click()
            actions.perform()
            time.sleep(1)

            theme_choice = self.bym_extract_data["theme"][0]
            theme_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in theme_element:
                if theme_choice in div_tag.text:
                    div_tag.click()
                    break
        theme = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[3]/div[5]/div/div[2]/div/div/div/div/div/div/div/span[1]/div[1]")
        self._scroll_display(theme, 50)

    def _write_tag(self):
        tag_list_btn = self.driver.find_elements_by_class_name('bmm-c-ico-list-search')[1]
        tag_list_btn.click()
        # tag一覧を取得
        tag_list_element = self.driver.find_elements_by_class_name("bmm-c-checkbox--tag")

        time.sleep(2)
        check_tag_list = self.bym_extract_data["tag"]
        check_tag_len = len(check_tag_list)
        tag_count = 0
        for div_tag in tag_list_element:
            if div_tag.text in check_tag_list:
                # その国を選択する
                # div_tag.click()
                self.driver.execute_script("arguments[0].click();", div_tag)
                tag_count += 1
                if tag_count == check_tag_len:
                    break

        next_btn = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[2]/div[7]/div/div/div[3]/button[2]')
        next_btn.click()
        self._scroll_display(tag_list_btn, 200)

    def _write_color(self):
        if len(self.bym_extract_data["color"]) > 0:
            color_num = 0
            dict = {}
            for colors in self.bym_extract_data["color"]:
                label = colors[0]
                color = colors[1]
                dict[color_correspondence_dict[label]] = color

            color_len = len(dict.keys())
            for color_cate, color_detail in dict.items():
                color_num += 1
                if color_num ==1:
                    color_box = self.driver.find_element_by_class_name("sell-color-option")
                else:
                    color_box = self.driver.find_element_by_xpath(
                        "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[" + str(
                            color_num) + "]/td[2]/div/div/span[1]/div[1]/span/div")

                # プルダウンをクリックし選択肢一覧を表示させる
                actions = ActionChains(self.driver)
                actions.move_to_element(color_box)
                actions.click()
                actions.perform()
                time.sleep(1)

                color_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')
                for div_tag in color_element:
                    if div_tag.text == color_cate:
                        # その国を選択する
                        div_tag.click()
                        break

                color_name_path = "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div[2]/table/tbody/tr[" + str(
                    color_num) + "]/td[3]/div/div/input"
                color_name = self.driver.find_element_by_xpath(color_name_path)
                color_name.send_keys(color_detail)

                if color_num < color_len:
                    self._scroll_display(color_name, 20)
                    add_color_btn = self.driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div[3]/a/i')
                    add_color_btn.click()
                else:
                    self._scroll_display(color_name, -color_len*20)

    def _write_size(self):
        size_tab = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/ul/li[2]")
        size_tab.click()

        # spanの中にある、「選択してください」って書いてあるdivパスを取得
        size_val = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/span[1]/div[1]")

        # プルダウンをクリックし選択肢一覧を表示させる
        actions = ActionChains(self.driver)
        actions.move_to_element(size_val)
        actions.click()
        actions.perform()
        time.sleep(1)

        size_list = self.lv_extract_data["size_list"]
        size_len = len(size_list)
        if size_len > 0:
            size_val_choice = "バリエーションあり"
        else:
            size_val_choice = "バリエーションなし"
        size_val_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

        for div_tag in size_val_element:
            if size_val_choice == div_tag.text:
                div_tag.click()
                break

        if size_val_choice == "バリエーションあり":
            size_num = 0
            for size in size_list:
                size_num += 1
                size_path = "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[2]/table/tbody/tr[" + str(
                    size_num) + "]/td[2]/div/div/div/input"
                size_name = self.driver.find_element_by_xpath(size_path)
                size_name.send_keys(size)

                if size_num < size_len:
                    self._scroll_display(size_name, 30)
                    # add_size_btn = self.driver.find_element_by_class_name('bmm-c-ico-plus')
                    add_size_btn = self.driver.find_element_by_xpath(
                        '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div[2]/div/div/div[3]/a/i')

                    add_size_btn.click()

    def _write_prod_num(self):
        prod_num = self.driver.find_element_by_xpath(
            '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/input')
        # id入力し、Enterキーを押下
        prod_num.send_keys("2")
        self._scroll_display(prod_num, 50)

    def _write_prod_code(self):
        prod_code_list = self.lv_extract_data["prod_code_list"]
        prod_code_len = len(prod_code_list)
        prod_code_num = 0
        for prod_no in prod_code_list:
            prod_code_num += 1

            prod_no_box_path = "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[3]/div/div[2]/div/div/div[2]/table/tbody/tr[" + str(
                prod_code_num) + "]/td[1]/input"
            prod_no_box = self.driver.find_element_by_xpath(prod_no_box_path)
            prod_no_box.send_keys(prod_no)

            loc = prod_no_box.location
            self.scroll_start = loc["y"]
            if prod_code_num < prod_code_len:
                self._scroll_display(prod_no_box, 20)
                add_prod_no_btn = self.driver.find_element_by_xpath(
                    '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[4]/div[3]/div/div[2]/div/div/div[3]/a/i')
                add_prod_no_btn.click()
            else:
                self._scroll_display(prod_no_box, 600, 2)
        time.sleep(2)

    def _write_delivery_method(self):
        place_list = self.bym_extract_data["palace"]
        if place_list[0] in prefecture_ep:
            delivery_area_list = ["ヨーロッパ", place_list[0]]
        elif place_list[0] in prefecture_ja:
            delivery_area_list = ["日本",  place_list[0]]
        else:
            delivery_area_list = ["ヨーロッパ", place_list[0]]

        delivery_area = delivery_area_list[0]
        if delivery_area == "日本":
            del_method_btn = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[6]/div/div/div[2]/div/div/div[2]/div[1]/table/tbody/tr[12]/td[2]')
        else:
            del_method_btn = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[6]/div/div/div[2]/div/div/div[2]/div[1]/table/tbody/tr[9]/td[2]')

        # 配送方法をクリック
        actions = ActionChains(self.driver)
        actions.move_to_element(del_method_btn)
        actions.click()
        actions.perform()
        self._scroll_display(del_method_btn, 50)

    def _write_buy_dead_line(self):
        dead_line_element = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div/input")
        dead_line = (datetime.date.today() + datetime.timedelta(days=14)).strftime('%Y/%m/%d')
        # 一度デフォルト入力を削除
        dead_line_element.click()
        text = dead_line_element.get_attribute("value")
        dead_line_element.send_keys(Keys.BACKSPACE * len(text))
        time.sleep(1)
        dead_line_element.send_keys(dead_line)
        time.sleep(1)

        # 購入期限カレンダーで隠れてるので、いったん適当なところをクリック
        actions = ActionChains(self.driver)
        actions.move_to_element(dead_line_element)
        actions.move_to_element_with_offset(dead_line_element, 600, 0)
        actions.click()
        actions.perform()
        time.sleep(1)
        self._scroll_display(dead_line_element, 50)

    def _write_buy_area(self):
        place_list = self.bym_extract_data["palace"]
        if place_list[0] in prefecture_ep:
            delivery_area_list = ["ヨーロッパ", place_list[0]]
        elif place_list[0] in prefecture_ja:
            delivery_area_list = ["日本", place_list[0]]
        else:
            delivery_area_list = ["ヨーロッパ", place_list[0]]

        delivery_area = delivery_area_list[1]
        if delivery_area in prefecture_ja:
            # 国内をチェック
            buy_area_btn = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[1]/div/label[1]/span")
            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(buy_area_btn)
            actions.click()
            actions.perform()

            time.sleep(1)
            # 都道府県を選択するためにプルダウン部分を取得
            area_category = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[2]/div/div/div/div/span[1]/div[1]')

            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(area_category)
            actions.click()
            actions.perform()
            time.sleep(1)

            area_category_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in area_category_element:
                if div_tag.text == delivery_area:
                    # その国を選択する
                    div_tag.click()
                    break

        else:
            buy_area_btn = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[1]/div/label[2]/span")
            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(buy_area_btn)
            actions.click()
            actions.perform()
            time.sleep(1)

            # 州を選択するためにプルダウン部分を取得
            area_category1 = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/span[1]/div[1]')

            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(area_category1)
            actions.click()
            actions.perform()
            time.sleep(1)

            area_category_element1 = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in area_category_element1:
                if div_tag.text == delivery_area_list[0]:
                    # その州を選択する
                    div_tag.click()
                    break

            area_category2 = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[2]/div/div[2]/div/div[2]/div/div[2]/div/div/span[1]/div[1]')
            # time.sleep(2)

            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(area_category2)
            actions.click()
            actions.perform()
            time.sleep(1)

            area_category_element2 = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in area_category_element2:
                if div_tag.text == delivery_area_list[1]:
                    # その国を選択する
                    div_tag.click()
                    break

    def _write_shop(self):
        shop_element = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[3]/div/div[2]/div/div/div/div/div[1]/input")
        shop_element.send_keys("Louis Vuitton 正規店")

        loc = shop_element.location
        self.scroll_start = loc["y"]
        self.scroll_goal = self.scroll_start + 30
        js_command = "window.scrollTo(" + str(self.scroll_start) + ", " + str(self.scroll_goal) + ");"
        self.driver.execute_script(js_command)
        time.sleep(1)

    def _write_send_area(self):
        place_list = self.bym_extract_data["palace"]
        if place_list[0] in prefecture_ep:
            delivery_area_list = ["ヨーロッパ", place_list[0]]
        elif place_list[0] in prefecture_ja:
            delivery_area_list = ["日本", place_list[0]]
        else:
            delivery_area_list = ["ヨーロッパ", place_list[0]]

        delivery_area = delivery_area_list[1]
        if delivery_area in prefecture_ja:
            # 国内をチェック
            send_area_btn = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[1]/div/label[1]/span")
            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(send_area_btn)
            actions.click()
            actions.perform()

            time.sleep(1)
            # 都道府県を選択するためにプルダウン部分を取得
            area_category = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[2]/div/div/div/div/span[1]/div[1]')

            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(area_category)
            actions.click()
            actions.perform()
            time.sleep(1)

            area_category_element = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in area_category_element:
                if div_tag.text == delivery_area:
                    # その国を選択する
                    div_tag.click()
                    break

        else:
            send_area_btn = self.driver.find_element_by_xpath(
                "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[1]/div/label[2]/span")
            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(send_area_btn)
            actions.click()
            actions.perform()
            time.sleep(1)

            # 州を選択するためにプルダウン部分を取得
            area_category1 = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[2]/div/div[1]/div/div/span[1]/div[1]')

            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(area_category1)
            actions.click()
            actions.perform()
            time.sleep(1)

            area_category_element1 = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in area_category_element1:
                if div_tag.text == delivery_area_list[0]:
                    # その州を選択する
                    div_tag.click()
                    break

            area_category2 = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[7]/div[4]/div/div[2]/div/div[2]/div/div[2]/div/div/span[1]/div[1]')
            # time.sleep(2)

            # プルダウンをクリックし選択肢一覧を表示させる
            actions = ActionChains(self.driver)
            actions.move_to_element(area_category2)
            actions.click()
            actions.perform()
            time.sleep(1)

            area_category_element2 = self.driver.execute_script('return document.getElementsByClassName("Select-option")')

            for div_tag in area_category_element2:
                if div_tag.text == delivery_area_list[1]:
                    # その国を選択する
                    div_tag.click()
                    break

    def _write_price(self):
        price_str = self.bym_extract_data["price"]
        price_str = price_str.replace('¥', '')
        price_str = price_str.replace(',', '')
        price = int(price_str) - 300

        price_element = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[8]/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div/input")
        price_element.send_keys(str(price))

    def _write_memo(self):
        message = datetime.date.today().strftime('%Y/%m/%d') + " タグチ" + "/" + self.exhbit_no
        message_element = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[9]/div[1]/div/div[2]/div/div[1]/textarea")
        message_element.send_keys(message)

    def _comp_btn(self):
        comp_btn_element = self.driver.find_element_by_xpath(
            "/html/body/div[3]/div[3]/div[1]/div/div[1]/div/div/div/div[2]/form/div[10]/div/button[1]")
        time.sleep(3)
        comp_btn_element.click()


    def extract_data_dict(self):
        return self.bym_extract_data, self.lv_extract_data


if __name__ == '__main__':
    BYM_INDEX = 0
    LV_INDEX = 1
    MESSAGE_INDEX = 2
    COUNTRY_INDEX = 3

    # log_id = "reimero2525@gmail.com"
    # log_pass = "2525reina"
    log_id = "tanabe.naoto3@gmail.com",
    log_pass = "n0313123",

    url_lists = [
                ["https://www.buyma.com/item/64556586/?af=4018",
                "https://en.louisvuitton.com/eng-nl/products/monogram-essential-bucket-hat-nvprod2550155v#M76586", "", ""],
                #  ["https://www.buyma.com/item/65579078/?ba_af=recommend_at_itemdetail",
                # "https://uk.louisvuitton.com/eng-gb/products/amazone-slingbag-monogram-other-nvprod2380063v", "", ""],
                # ["https://www.buyma.com/item/66463914/",
                # "https://uk.louisvuitton.com/eng-gb/products/monogram-watercolour-skater-hat-nvprod2810044v", "", ""],
                # ["https://www.buyma.com/item/62784749/",
                # "https://en.louisvuitton.com/eng-nl/products/monogram-essential-bucket-hat-nvprod2550155v#M76586", "", ""],
                # ["https://www.buyma.com/item/58513475/?ba_af=recommend_at_itemdetail",
                # "https://uk.louisvuitton.com/eng-gb/products/keepall-bandouliere-45-monogram-macassar-000206", "", ""],
                # ["https://www.buyma.com/item/65825055/?ba_af=recommend_at_itemdetail",
                # "https://en.louisvuitton.com/eng-nl/products/onthego-gm-tote-bag-nvprod2800059v", "", ""],
                ]

    conter = 7
    dt_now = datetime.datetime.now()
    now = dt_now.strftime('%Y%m%d-%H%M')

    log_dir = "C:\\Users\\ntagu\\workspace\\til\\web_op\\exhibition_page_create_bym\\log\\"
    log_path = log_dir + now + ".log"
    write_mode = "w"
    for url in url_lists:
        exhbt_no = str(conter)
        bym_collector = BymExhibitionPageCreater(ref_bym_url=url[BYM_INDEX],
                                                 lv_url=url[LV_INDEX],
                                                 exhbt_no=exhbt_no,
                                                 title_msg=url[MESSAGE_INDEX],
                                                 country=url[COUNTRY_INDEX],
                                                 login_id=log_id,
                                                 login_pass=log_pass,
                                                 )
        bym_dict, lv_dict = bym_collector.extract_data_dict()

        if not os.path.exists(log_dir):
            # ディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(log_dir)
        with open(log_path, write_mode, encoding="utf-8") as f:
            print(exhbt_no, "===============\n", file=f)
            for key, value in bym_dict.items():
                print("{} : {}".format(key, value), file=f)
            for key, value in lv_dict.items():
                print("{} : {}".format(key, value), file=f)
            print("\n", file=f)
            write_mode = "a"
        conter +=1
        print("exhbt_no:", exhbt_no, "\n")