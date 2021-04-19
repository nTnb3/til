from requests_html import HTMLSession
import time
from bs4 import BeautifulSoup

from selenium import webdriver
import chromedriver_binary


class ChnlPageDataCollector(object):
    def __init__(self, prod_url, prod_code_list):
        """

        :param en_prod_url:
        :param jp_prod_tmp_url:
        """
        self.prod_url = prod_url
        self.prod_code_list = prod_code_list
        self._data_dict = {}
        self._ready_scraping(prod_url)
        self.check_page = self._check_lv_page()

        if self.check_page:
            print("not found chnl page")
            for key in self._data_dict.keys():
                self._data_dict[key] = "not found lv page"
            self._data_dict["is_enable"] = False
        else:
            self._fetch_data()
            self._data_dict["is_enable"] = True

    def _ready_scraping(self, prod_url):
        # セッション開始
        session = HTMLSession()
        self.r = session.get(prod_url)

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
        # self._data_dict["prod_code"] = self._fetch_prod_code()
        self._data_dict["prod_code_list"] = self.prod_code_list
        self._data_dict["prod_spec"] = self._fetch_prod_spec()
        # self._data_dict["size_list"] = self._fetch_size_list()
        # self._data_dict["size_table"] = self._fetch_size_table()
        # self._data_dict["color_list"] = self._fetch_color_list()

    def _fetch_prod_name(self):
        time.sleep(2)
        prod_name = self.r.html.find('.fs-productsheet__title')
        return prod_name[0].text

    def _fetch_prod_code(self):
        time.sleep(2)
        product_code = self.r.html.find('.fs-productsheet__ref')
        product_code_str = product_code[0].text.split(':')[-1]
        return product_code_str

    def _fetch_prod_code_list(self):
        time.sleep(2)
        # 入力リストから取得
        product_code_list = []
        product_codes_e = self.r.html.find('.slick-list')
        # AP2033 B05060 94305 ⇐ こんな感じ
        # <a>のdata-datalayer={data-id="ap2033b05060nb354"}に入っている
        for e in product_codes_e:
            product_code_list.append(e.attrs["id"].split('-')[-1])
        if len(product_code_list) == 0:
            product_code_list.append(self._data_dict["prod_code"])
        return product_code_list

    def _fetch_prod_spec(self):
        time.sleep(2)
        prod_spec = self.r.html.find('.fs-size__label')
        proc_space_text = prod_spec[0].text
        return proc_space_text

    def _fetch_size_list(self):
        # 洋服のサイズ表が見つからないので一旦スキップ
        time.sleep(2)
        size = self.r.html.find('.lv-product-panel-list__item-name')
        size_list = []
        for e in size:
            text = e.text
            if text[0] == "0":
                text = text[1:]
            size_list.append(text)
        return size_list

    def _fetch_color_list(self):
        # buyma参考ページから取得
        time.sleep(2)
        self._activate_browser()
        color_e = self.driver.execute_script('return document.querySelector("#main-wrapper > section > div > div.fs-productsheet__main.fs-price__mentioncontainer.fs-price__mentioncontainer--hasPrice > div.fs-productsheet__details > div.fs-productsheet__details-content > div.slick-loaded > div.fs-productsheet__section.fs-productsheet__materials-section > div > div > ul > div > div")')
        # color_e = self.driver.execute_script('return document.getElementsByClassName("slick-track")')
        # color = self.r.html.find('.lv-product-card__url')
        color_list = []
        for e in color_e:
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

        table_str = ""
        if is_table:
            # BeautifulSoupでhtmlをパース
            soup = BeautifulSoup(html, "html.parser")
            # table取得
            table = soup.findAll("table", {"class": "lv-size-guide-table__table"})[0]
            rows = table.findAll("tr")
            row_count = 0
            header = 0
            for row in rows:
                csvRow = ""
                if row_count == header:
                    for cell in row.findAll(['td', 'th']):
                        cell_str = cell.get_text()
                        cell_str = cell_str.replace('\n', '')
                        cell_str = cell_str.replace(' ', '')
                        cell_str += ' / '
                        csvRow += cell_str
                else:
                    for cell in row.findAll(['td', 'th']):
                        cell_str = cell.get_text()
                        cell_str += ' / '
                        csvRow += cell_str
                csvRow = csvRow[:-3]
                csvRow += "\n"
                table_str += csvRow
                row_count += 1
        return table_str

    def _activate_browser(self):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(self.prod_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()

    def _check_lv_page(self):
        try:
            check = self.r.html.find('.search-no-result-title')
            check_list = []
            for e in check:
                check_list.append(e.get_text())
            if "該当項目が見つかりません。検索キーワード：" in check_list[0]:
                return True
            else:
                return False
        except:
            return False


if __name__ == '__main__':
    URL = 0
    PROD_CODE_LIST = 1
    prod_input_list = [["https://www.chanel.com/ja_JP/fashion/p/slg/ap2033b05060/ap2033b0506094305/phone-airpods-case-with-chain-grained-calfskin-laquered-goldtone-metal-black.html", ["AP2033 B05060 94305", "AP2033 B05060 NB354"]]]
    is_bag = True
    for prod_input in prod_input_list:
        chnl_collector = ChnlPageDataCollector(prod_url=prod_input[URL], prod_code_list=prod_input[PROD_CODE_LIST])

        lv_extract_data = chnl_collector.data_dict
        for key, value in lv_extract_data.items():
            print("{} : {}".format(key, value))
        print("\n")
