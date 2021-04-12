from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from selenium import webdriver


class BymPageDataCollector(object):
    def __init__(self, ref_bym_url):
        self.ref_bym_url = ref_bym_url
        self._ready_scraping()

    def _ready_scraping(self):
        session = HTMLSession()
        r = session.get(self.ref_bym_url)
        self.soup = BeautifulSoup(r.text, 'html.parser')

    def _fetch_category_data(self):
        # カテゴリをselectorから取得
        category = self.soup.select("#s_cate > dd > a")

    def _fetch_season_data(self):
        # シーズンをselectorから取得
        season = self.soup.select("#s_season > dd > a")

    def _fetch_theme_data(self):
        # テーマをselectorから取得
        theme = self.soup.select("dt:contains(""テーマ"") ~ dd")

    def _fetch_tag_data(self):
        # タグをselectorから取得
        tag = self.soup.select(
            '#detail_wrap > div.detail_main > div.n_common_tabwrap.fab-design-mg--t30.fab-design-mg--b40 > \
            div > div.js-itemcomment-disc.itemcomment-disc.itemcomment-disc--l.fab-design-mg--r20.fab-design-pg--r20 > \
            div > ul > li')

    def _fetch_buying_place(self):
        # 発送地をselectorから取得
        buying_country = self.soup.select("#s_buying_area > dd > img")
        buying_area = self.soup.select("#s_buying_area > dd > a")

    def _fetch_price(self):
        # 価格
        price = self.soup.select("#abtest_display_pc")

    def _fetch_img(self, save_path='./img/'):
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

        for i, image in enumerate(srcs):
            re = requests.get(image)
            i += 100
            path = save_path + f'{i}.' + image.split('.')[-1]
            with open(path, 'wb') as f:
                f.write(re.content)

    def _activate_browser(self):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(self.ref_bym_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()