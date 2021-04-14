from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver


class LvPageDataCollector(object):
    def __init__(self, en_prod_url, jp_prod_tmp_url="https://jp.louisvuitton.com/jpn-jp/search/"):
        self._ready_scraping(en_prod_url, jp_prod_tmp_url)

    def _ready_scraping(self, en_prod_url, jp_prod_tmp_url):
        # セッション開始
        session = HTMLSession()
        r = session.get(en_prod_url)
        self._access_jp_page(r, session, jp_prod_tmp_url)

    def _access_jp_page(self, r, sess, jp_prod_tmp_url):
        # 外国語ページから型番をclassから取得
        product_no = self._fetch_prod_no()
        # 取得した型番から日本語版ページにアクセスする
        jp_prod_url = jp_prod_tmp_url + product_no
        self.r = sess.get(jp_prod_url)

    def _fetch_prod_name(self):
        prod_name = self.r.html.find('.lv-product__title')
        return prod_name[0].text

    def _fetch_prod_no(self):
        product_no = self.r.html.find('.lv-product__details-sku')
        return product_no[0].text

    def _fetch_prod_spec(self):
        prod_spec = self.r.html.find('#read-more')
        return prod_spec[0].text

    def _fetch_size_list(self):
        size = self.r.html.find('.lv-product-panel-list__item-name')
        size_list = []
        for e in size:
            size_list.append(e.text)
        return size_list

    def _fetch_color_list(self):
        color = self.r.html.find('.lv-product-card__url')
        color_list = []
        for e in color:
            color_list.append([e.text])
        return color_list

    def _fetch_size_table(self):
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

    def _activate_browser(self):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(self.ref_bym_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()