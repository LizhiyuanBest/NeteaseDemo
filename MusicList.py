# -*- coding=utf-8 -*

# 0.导入框架
import requests
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

# 5.拿到外链
base_url = 'https://link.hhtjim.com/163/'  # + 1369601580.mp3

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

# url = 'http://music.163.com/song/media/outer/url?id='  # 1369601580  另一种下载接口
COUNT = 10000
# 建立歌曲存放文件夹
if not os.path.exists("./music"):
    os.mkdir("./music/")

try:
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 不弹窗
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    wait = WebDriverWait(driver, 5)
except Exception as e:
    print("请先安装最新版Chrome浏览器!", e)

file_handle = open('music_menu.txt', mode='w')

url = 'https://music.163.com/#/discover/playlist'
titles = []
hrefs = []
while url != 'javascript:void(0)':
    driver.get(url)
    driver.switch_to.frame("g_iframe")  # 进入新的页面，新的框架， 不然下面的是得不到信息的
    names = driver.find_elements_by_xpath('//ul[@class="m-cvrlst f-cb"]/li')
    # print(names)
    for li in names:  # 遍历得到歌单的名字和网址
        title = li.find_element_by_xpath('.//p[@class="dec"]/a').get_attribute('title')
        href = li.find_element_by_xpath('.//p[@class="dec"]/a').get_attribute('href')
        file_handle.write('{}  {} \n'.format(title, href))
        print(title, href)
        titles.append(title)
        hrefs.append(href)
    url = driver.find_element_by_xpath('//*[@id="m-pl-pager"]/div/a[11]').get_attribute('href')
file_handle.close()

file_handle = open('music_list.txt', mode='w')
names = []
ids = []
count = 0
for title, href in zip(titles, hrefs):
    try:
        if not os.path.exists("./music/%s" % title):  # 安装歌单建立文件夹
            os.mkdir("./music/%s" % title)
        else:
            continue
    except:
        print('folder error music/{}'.format(title))
        continue

    driver.get(href)
    driver.switch_to.frame("g_iframe")  # 进入新的框架
    trs = driver.find_elements_by_xpath('//tbody/tr')
    # print(trs)
    for tr in trs:  # 遍历得到歌名和id
        song_name = tr.find_element_by_xpath('.//span[@class="txt"]/a/b').get_attribute('title')
        song_id = tr.find_element_by_xpath('.//span[@class="txt"]/a').get_attribute('href')
        names.append(song_name)
        ids.append(song_id)
        file_handle.write('{}  {} {}\n'.format(title, song_name, song_id))
        # 得到歌曲的id
        song_id = song_id.split('=')[-1]
        # print(song_name, song_id)

        ''' 第一种方法 下载的mp3打不开
        # song_url = 'http://music.163.com/song/media/outer/url?id={}.mps'.format(song_id)
        # path = './music/{}/{}.mp3'.format(title, song_name)

        # try:  # 保存
        #     urlretrieve(song_url, path)
        #     print('{} Successful {}/{}.mp3'.format(count, title, song_name))
        # except:
        #     print('{} error {}/{}.mp3'.format(count, title, song_name))
        '''

        # 去外链地址拿到歌曲的二进制文件
        music_url = base_url + '%s' % song_id + '.mp3'
        # music = requests.get(music_url).content

        try:  # 保存
            music = requests.get(music_url, headers=headers, timeout=20)
            with open('./music/{}/{}.mp3'.format(title, song_name), 'wb') as file:
                file.write(music.content)
                print('{} Successful {}/{}.mp3'.format(count, title, song_name))
                count += 1
        except:
            print('{} error {}/{}.mp3'.format(count, title, song_name))
        sleep(0.02)
        # count += 1

    if count >= COUNT:
        break
file_handle.close()



