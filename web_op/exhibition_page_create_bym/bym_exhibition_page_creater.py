import datetime

from selenium import webdriver
import chromedriver_binary

from .bym_page_data_collector import BymPageDataCollector
from .lv_page_data_collector import LvPageDataCollector

from create_ja_area_list import prefecture


class BymExhibitionPageCreater(object):
    def __init__(self, ref_bym_url, lv_url, title_msg, exhbt_no, exhibition_url):
        self.title_msg = title_msg

        dt_now = datetime.datetime.now()
        today = dt_now.strftime('%m-%d')
        self.bym_data_collector = BymPageDataCollector(ref_bym_url, today, exhbt_no)
        bym_extract_data = self.bym_data_collector.data_dict
        self.lv_data_collector = LvPageDataCollector(lv_url)
        lv_extract_data = self.lv_data_collector.data_dict

    def _activate_browser(self, exhibition_url):
        # ブラウザを起動する
        self.driver = webdriver.Chrome()
        # ブラウザでアクセスする
        self.driver.get(exhibition_url)

    def _close_browser(self):
        # ブラウザを閉じる
        self.driver.quit()