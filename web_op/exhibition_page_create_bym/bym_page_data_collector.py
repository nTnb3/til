from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver


class BymPageDataCollector(object):
    def __init__(self, ref_bym_url, today, exhbt_no, save_root_path="./img"):
        self.ref_bym_url = ref_bym_url
        self._data_dict = {}
        self._ready_scraping()
        self._init_data_dict()
        self._fetch_data(today, exhbt_no, save_root_path)

    def _init_data_dict(self):
        data_label = ["category",
                      "season",
                      "theme",
                      "tag",
                      "palace",
                      "price",
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
        self._data_dict["img_path"] = self._fetch_img(today, exhbt_no, save_root_path)

    def _fetch_category_data(self):
        # カテゴリをselectorから取得
        category = self.soup.select("#s_cate > dd > a")
        category_list = []
        for e in category:
            category_list.append(e.get_text())
        return category_list

    def _fetch_season_data(self):
        # シーズンをselectorから取得
        season = self.soup.select("#s_season > dd > a")
        for e in season:
            s = e.get_text()
        return s

    def _fetch_theme_data(self):
        # テーマをselectorから取得
        theme = self.soup.select("dt:contains(""テーマ"") ~ dd")
        theme_list = []
        for e in theme:
            theme_list.append(e.get_text())
        return theme_list

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
        for e in buying_country:
            c = e.get_text()
        buying_area = self.soup.select("#s_buying_area > dd > a")
        for e in buying_area:
            a = e.get_text()
        place_list = [c, a]
        return place_list

    def _fetch_price_data(self):
        # 価格
        price = self.soup.select("#abtest_display_pc")
        for e in price:
            p = e.get_text()
        return p

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

        save_dir_path = save_root_path + today + exhbt_no + '/'
        for i, image in enumerate(srcs):
            re = requests.get(image)
            i += 100
            save_path = save_dir_path + f'{i}.' + image.split('.')[-1]
            with open(save_path, 'wb') as f:
                f.write(re.content)
        return save_dir_path

    def _activate_browser(self):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(self.ref_bym_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()