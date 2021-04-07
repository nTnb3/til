import pandas as pd


# Webページを取得して解析する
# url = "https://jp.louisvuitton.com/jpn-jp/products/pochette-melanie-mm-monogram-empreinte-nvprod2020033v#M68707"
# url = "https://jp.louisvuitton.com/jpn-jp/products/placed-graphic-shirt-nvprod2550073v"
url = "https://www.buyma.com/item/52558726/"

data = pd.read_html(url, header=0)

print(data)