# -*- coding=utf-8 -*

# 导入框架
import requests
from fake_useragent import UserAgent
from lxml import etree
import os
from time import sleep
from urllib.request import urlretrieve
from selenium import webdriver
from selenium.webdriver.common.keys import Keys  # 输入框回车
from selenium.webdriver.common.by import By  # 与下面的2个都是等待时要用到
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # 异常处理
from selenium.webdriver.chrome.options import Options

# 网易云外链地址
base_url = 'https://link.hhtjim.com/163/'  # + 1369601580.mp3

ua = UserAgent()  # 实例化
print(ua.chrome)  # 获取谷歌浏览器的headers，每次打印结果是不一样的
# 请求头就可以写成
headers = {"User-Agent": ua.random}

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
#              AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

# 建立歌曲存放文件夹
if not os.path.exists("./music"):
    os.mkdir("./music/")


try:
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 不弹窗
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    wait = WebDriverWait(driver, 15)
except Exception as e:
    print("请先安装最新版Chrome浏览器!", e)

url = 'https://music.163.com/#/discover/toplist?id=3778678'


count = 0
# 建立歌曲存放文件夹
if not os.path.exists("./music/Hot Music/"):
    os.mkdir("./music/Hot Music/")

driver.get(url)
driver.switch_to.frame("g_iframe")  # 进入新的框架
trs = driver.find_elements_by_xpath('//tbody/tr')
# print(trs)
for tr in trs:  # 遍历得到歌名和id
    song_name = tr.find_element_by_xpath('.//span[@class="txt"]/a/b').get_attribute('title')
    song_id = tr.find_element_by_xpath('.//span[@class="txt"]/a').get_attribute('href')

    # 得到歌曲的id
    song_id = song_id.split('=')[-1]
    # print(song_name, song_id)

    # 去外链地址拿到歌曲的二进制文件
    music_url = base_url + '%s' % song_id + '.mp3'
    # music = requests.get(music_url).content

    try:  # 保存
        music = requests.get(music_url, headers=headers, timeout=20)
        with open('./music/Hot Music/{}.mp3'.format(song_name), 'wb') as file:
            file.write(music.content)
            print('{} Successful {}.mp3'.format(count, song_name))
            count += 1
    except:
        print('{} error {}.mp3'.format(count, song_name))
    sleep(0.05)






