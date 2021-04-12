from selenium import webdriver

from .bym_page_data_collector import BymPageDataCollector
from .lv_page_data_collector import LvPageDataCollector

from create_ja_area_list import prefecture


class BymExhibitionPageCreater(object):
    def __init__(self, exhibition_url, ref_bym_url, lv_url, title_msg):
        self.title_msg = title_msg
        self.bym_data_collector = BymPageDataCollector(ref_bym_url)
        self.lv_data_collector = LvPageDataCollector(lv_url)

    def _activate_browser(self, exhibition_url):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(exhibition_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()