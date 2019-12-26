import selenium

# from bs4 import BeautifulSoup
# from selenium import webdriver
# url='https://search.jd.com/Search?keyword=%E7%BE%BD%E7%BB%92%E6%9C%8D&enc=utf-8&wq=yu%27rong%27fu&pvid=32ac7af897f04e48ad574347f2816650'
# driver = webdriver.Chrome()
# driver.get(url=url)
# text=driver.page_source
# driver.close()
# soup=BeautifulSoup(text,'lxml')
# titel=soup.select('#J_promGoodsWrap_291 > div.mc > ul > li:nth-child(4) > div > a > div > em')
# for i in titel:
#     print(i.get_text())

import requests
adders='https://search.jd.com/Search?keyword=%E7%BE%BD%E7%BB%92%E6%9C%8D&enc=utf-8&wq=yu%27rong%27fu&pvid=32ac7af897f04e48ad574347f2816650'
reson=requests.get(url=adders)
print(reson)
print(reson.text)