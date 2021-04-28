import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains


url = "https://en.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-luxembourg-trainer-shoes--BGGU1PMOEC_PM2_Front%20view.png?wid=1080&hei=1080"
# url = "https://jp.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-%E3%83%9D%E3%82%B7%E3%82%A7%E3%83%83%E3%83%88%E3%83%BB%E3%82%B3%E3%82%B9%E3%83%A1%E3%83%86%E3%82%A3%E3%83%83%E3%82%AF-%E3%83%A2%E3%83%8E%E3%82%B0%E3%83%A9%E3%83%A0%E3%83%BB%E3%82%A2%E3%83%B3%E3%83%97%E3%83%A9%E3%83%B3%E3%83%88-%E3%83%88%E3%83%A9%E3%83%99%E3%83%AB--M80502_PM2_Front%20view.png"
# url = url[:url.find("png")+3]

file_name = "sample-img2.jpg"
opt = webdriver.ChromeOptions()
opt.add_argument('--blink-settings=imagesEnabled=true')
driver = webdriver.Chrome(options=opt)
# ブラウザでアクセスする
# driver.get("https://jp.louisvuitton.com/images/is/image/lv/1/PP_VP_L/louis-vuitton-%E3%83%AB%E3%82%AF%E3%82%BB%E3%83%B3%E3%83%96%E3%83%AB%E3%82%B0%E3%83%BB%E3%83%A9%E3%82%A4%E3%83%B3-%E3%82%B9%E3%83%8B%E3%83%BC%E3%82%AB%E3%83%BC-%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA--BGGU1PMOEC_PM2_Front%20view.png?wid=2048&hei=2048")
driver.get("https://jp.louisvuitton.com/jpn-jp/products/luxembourg-sneaker-nvprod1270499v#1A4PAV")
import urllib.request
# ... (省略) ...
# url = driver.find_element_by_class_name("lv-smart-picture__object").get_attribute("src")
imgs = driver.find_elements_by_class_name("lv-slider__container")

for img in imgs:
    actions = ActionChains(driver)
    actions.move_to_element(img)
    actions.click()
    actions.perform()
    time.sleep(2)

    img_src = driver.execute_script('return document.getElementsByClassName("lv - smart - picture__object")')




    print("wwww")
# urllib.request.urlretrieve(url, 'logo.png')




# # セッション開始
# session = HTMLSession()
# response = session.get(url)
# image = response.content
#
# with open(file_name, "wb") as aaa:
#     aaa.write(image)