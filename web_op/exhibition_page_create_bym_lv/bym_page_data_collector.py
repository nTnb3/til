import os
import shutil

from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver

# chromedriver_binaryのパスを通すimport
import chromedriver_binary

from util import convert_rgb

class BymPageDataCollector(object):
    def __init__(self, ref_bym_url, today, exhbt_no, save_root_path="./img/"):
        self.ref_bym_url = ref_bym_url
        self._data_dict = {}
        self._ready_scraping()
        self._init_data_dict()

        self.check_page = self._check_exhibition_page()
        if self.check_page:
            print("not found ref bym page")
            for key in self._data_dict.keys():
                self._data_dict[key] = "not found ref bym page"
            self._data_dict["is_enable"] = False
        else:
            self._fetch_data(today, exhbt_no, save_root_path)
            self._data_dict["is_enable"] = True

    def _init_data_dict(self):
        data_label = ["category",
                      "season",
                      "theme",
                      "tag",
                      "palace",
                      "price",
                      "color",
                      "img_path"]
        for label in data_label:
            self._data_dict[label] = None

    def _ready_scraping(self):
        session = HTMLSession()
        r = session.get(self.ref_bym_url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    @property
    def data_dict(self):
        return self._data_dict

    def _fetch_data(self, today, exhbt_no, save_root_path):
        self._data_dict["category"] = self._fetch_category_data()
        self._data_dict["season"] = self._fetch_season_data()
        self._data_dict["theme"] = self._fetch_theme_data()
        self._data_dict["tag"] = self._fetch_tag_data()
        self._data_dict["palace"] = self._fetch_buying_place_data()
        self._data_dict["price"] = self._fetch_price_data()
        self._data_dict["color"] = self._fetch_color()
        self._data_dict["img_path"] = self._fetch_img(today, exhbt_no, save_root_path)

    def _fetch_category_data(self):
        # カテゴリをselectorから取得
        category = self.soup.select("#s_cate > dd > a")
        category_list = []
        for e in category:
            category_list.append(e.get_text())
        if len(category_list) != 0:
            return category_list
        else:
            return []

    def _fetch_season_data(self):
        # シーズンをselectorから取得
        season = self.soup.select("#s_season > dd > a")
        s_list = []
        for e in season:
            s_list.append(e.get_text())
        if len(s_list) != 0:
            return s_list
        else:
            return []

    def _fetch_theme_data(self):
        # テーマをselectorから取得
        theme = self.soup.select("dt:contains(""テーマ"") ~ dd")
        theme_list = []
        for e in theme:
            theme_list.append(e.get_text())
        if len(theme_list) != 0:
            return theme_list
        else:
            return []

    def _fetch_tag_data(self):
        # タグをselectorから取得
        tag = self.soup.select(
            '#detail_wrap > div.detail_main > div.n_common_tabwrap.fab-design-mg--t30.fab-design-mg--b40 > \
            div > div.js-itemcomment-disc.itemcomment-disc.itemcomment-disc--l.fab-design-mg--r20.fab-design-pg--r20 > \
            div > ul > li')
        tag_list = []
        for e in tag:
            tag_list.append(e.get_text())
        return tag_list

    def _fetch_buying_place_data(self):
        # 発送地をselectorから取得
        buying_country = self.soup.select("#s_buying_area > dd > img")
        c_list = []
        for e in buying_country:
            c_list.append(e.attrs['alt'])
        buying_area = self.soup.select("#s_buying_area > dd > a")
        a_list = []
        for e in buying_area:
            a_list.append(e.get_text())
        place_list = [c_list[0], a_list[0]]
        return place_list

    def _fetch_price_data(self):
        # 価格
        price = self.soup.select("#abtest_display_pc")
        p_list = []
        for e in price:
            p_list.append(e.get_text())
        if len(p_list) != 0:
            return p_list[0]
        else:
            return []

    def _fetch_img(self, today, exhbt_no, save_root_path):
        # ブラウザ起動
        self._activate_browser()

        small_img_sel_path = '#detail_img > div.item-thumbs > ul > li'
        elements = self.driver.find_element_by_css_selector(small_img_sel_path)
        # 文字コードをUTF-8に変換
        html = self.driver.page_source.encode('utf-8')

        # BeautifulSoupでhtmlをパース
        soup = BeautifulSoup(html, "html.parser")

        # ブラウザを閉じる
        self._close_browser()

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

        save_dir_path = save_root_path + today + '_' + exhbt_no + '/'
        if not os.path.exists(save_dir_path):
            # ディレクトリが存在しない場合、ディレクトリを作成する
            os.makedirs(save_dir_path)
        is_copy_img = True
        num = 0
        for i, image in enumerate(srcs):
            if i >= 1:
                if is_copy_img:
                    shutil.copyfile("./img/img0.png", save_dir_path+"101.jpg")
                    convert_rgb(save_dir_path+"101.jpg")
                    num += 1
                    is_copy_img = False
            re = requests.get(image)
            save_path = save_dir_path + f'{num+100}.' + image.split('.')[-1]
            with open(save_path, 'wb') as f:
                f.write(re.content)
            num += 1
        return save_dir_path

    def _fetch_color(self):
        self._activate_browser()
        is_color = True
        try:
            element = self.driver.find_element_by_css_selector('#colorsize > div.colorsize_select.js-color-select').click()
        except:
            is_table = False
        # 文字コードをUTF-8に変換
        html = self.driver.page_source.encode('utf-8')

        # ブラウザを閉じる
        self._close_browser()

        # BeautifulSoupでhtmlをパース
        soup = BeautifulSoup(html, "html.parser")
        color = soup.select("#colorsize > div.colorsize_select.js-color-select > ul > li > span")
        count = 0
        color_list = []
        color_label_list = []
        for e in color:
            if count % 2 == 0:
                extract_color = e.attrs
                color_label = list(extract_color.values())[0][1]
                color_label_list.append(color_label)
            else:
                c = e.get_text()
                color_label_list.append(c)
                color_list.append(color_label_list)
                color_label_list = []
            count += 1
        return color_list

    def _activate_browser(self):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(self.ref_bym_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()

    def _check_exhibition_page(self):
        try:
            check = self.soup.find_all(class_="notfoundSection_txt")
            check_list = []
            for e in check:
                check_list.append(e.get_text())
            if check_list[0] == "申し訳ございません。お探しの商品は既に出品がとりやめられました。":
                return True
            else:
                return False
        except:
            return False


if __name__ == '__main__':
    import datetime
    ref_bym_url_list = ["https://www.buyma.com/item/58513475/?ba_af=recommend_at_itemdetail",
                        "https://www.buyma.com/item/62821396/?ba_af=recommend_at_itemdetail"]

    for ref_bym_url in ref_bym_url_list:
        dt_now = datetime.datetime.now()
        today = dt_now.strftime('%m-%d')
        exhbt_no = "①"
        bym_collector = BymPageDataCollector(ref_bym_url, today, exhbt_no)

        bym_extract_data = bym_collector.data_dict
        for key, value in bym_extract_data.items():
            print("{} : {}".format(key, value))
        print("\n")