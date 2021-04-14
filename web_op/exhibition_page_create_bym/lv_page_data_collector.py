from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver


class LvPageDataCollector(object):
    def __init__(self, en_prod_url, jp_prod_tmp_url="https://jp.louisvuitton.com/jpn-jp/search/"):
        """

        :param en_prod_url:
        :param jp_prod_tmp_url:
        """
        self._data_dict = {}
        self._ready_scraping(en_prod_url, jp_prod_tmp_url)
        self._fetch_data()
        self._data_dict["is_enable"] = True

    def _ready_scraping(self, en_prod_url, jp_prod_tmp_url):
        # セッション開始
        session = HTMLSession()
        self.r = session.get(en_prod_url)
        self.jp_prod_url = self._access_jp_page(session, jp_prod_tmp_url)

    def _access_jp_page(self, sess, jp_prod_tmp_url):
        # 外国語ページから型番をclassから取得
        product_code = self._fetch_prod_code()
        # 取得した型番から日本語版ページにアクセスする
        jp_prod_url = jp_prod_tmp_url + product_code
        self.r = sess.get(jp_prod_url)
        return jp_prod_url

    def _init_data_dict(self):
        data_label = ["prod_name",
                      "season",
                      "theme",
                      "tag",
                      "palace",
                      "price",
                      "img_path"]
        for label in data_label:
            self._data_dict[label] = None

    @property
    def data_dict(self):
        return self._data_dict

    def _fetch_data(self):
        self._data_dict["prod_name"] = self._fetch_prod_name()
        self._data_dict["prod_code"] = self._fetch_prod_code()
        self._data_dict["prod_code_list"] = self._fetch_prod_code_list()
        self._data_dict["prod_spec"] = self._fetch_prod_spec()
        self._data_dict["size_list"] = self._fetch_size_list()
        self._data_dict["size_table"] = self._fetch_size_table()

    def _fetch_prod_name(self):
        prod_name = self.r.html.find('.lv-product__title')
        return prod_name[0].text

    def _fetch_prod_code(self):
        product_code = self.r.html.find('.lv-product__details-sku')
        return product_code[0].text

    def _fetch_prod_code_list(self):
        product_code_list = []
        product_codes_e = self.r.html.find('.lv-product-card__name')
        for e in product_codes_e:
            product_code_list.append(e.attrs["id"].split('-')[-1])
        return product_code_list

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
        self._activate_browser()
        # サイズガイドを取得し、クリック
        is_table = True
        try:
            element = self.driver.find_element_by_class_name('lv-product-size-guide__button').click()
        except:
            is_table = False

        # 文字コードをUTF-8に変換
        html = self.driver.page_source.encode('utf-8')

        # ブラウザを閉じる
        self._close_browser()

        table_list = []
        if is_table:
            # BeautifulSoupでhtmlをパース
            soup = BeautifulSoup(html, "html.parser")
            # table取得
            table = soup.findAll("table", {"class": "lv-size-guide-table__table"})[0]
            rows = table.findAll("tr")
            for row in rows:
                csvRow = []
                for cell in row.findAll(['td', 'th']):
                    cell_str = cell.get_text()
                    cell_str = cell_str.replace('\n', '')
                    csvRow.append(cell_str)
                table_list.append(csvRow)
        return table_list

    def _activate_browser(self):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(self.jp_prod_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()


if __name__ == '__main__':
    en_prod_url_list = ["https://jp.louisvuitton.com/jpn-jp/products/lv-trainer-sneaker-nvprod2510017v#1A8KD8"]
    is_bag = True
    for en_prod_url in en_prod_url_list:
        lb_collector = LvPageDataCollector(en_prod_url)

        lv_extract_data = lb_collector.data_dict
        for key, value in lv_extract_data.items():
            print("{} : {}".format(key, value))
        print("\n")
