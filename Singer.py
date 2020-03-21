# -*- coding=utf-8 -*

import requests
from fake_useragent import UserAgent
import argparse
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# 下载网易云的歌手的歌曲，输入是专辑页面的URL，和专辑页面的数量，歌手名， 存放地址

# 外链
base_url = 'https://link.hhtjim.com/163/'  # + 1369601580.mp3

ua = UserAgent()  # 实例化
print(ua.chrome)  # 获取谷歌浏览器的headers，每次打印结果是不一样的
# 请求头就可以写成
headers = {"User-Agent": ua.random}

# 建立歌曲存放主文件夹
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


def download(url, singer_name, page_num=5, singer_path='./music/singer'):
    titles = []
    hrefs = []
    while url != 'javascript:void(0)':
        driver.get(url)
        driver.switch_to.frame("g_iframe")  # 进入新的页面，新的框架， 不然下面的是得不到信息的
        names = driver.find_elements_by_xpath('//ul[@class="m-cvrlst m-cvrlst-alb4 f-cb"]/li')
        # print(names)
        for li in names:  # 遍历得到歌单的名字和网址
            title = li.find_element_by_xpath('.//p[@class="dec dec-1 f-thide2 f-pre"]').get_attribute('title')
            href = li.find_element_by_xpath('.//p[@class="dec dec-1 f-thide2 f-pre"]/a').get_attribute('href')
            print(title, href)
            titles.append(title)
            hrefs.append(href)
        url = driver.find_element_by_xpath('//*[@class="u-page"]/a[%d+2]' % page_num).get_attribute('href')

    # 建立歌手歌曲存放主文件夹
    if not os.path.exists(singer_path):
        os.mkdir(singer_path)

    file_handle = open(os.path.join(singer_path, '{}_music_list.txt'.format(singer_name)), mode='w')
    count = 0  # 计数
    for title, href in zip(titles, hrefs):
        driver.get(href)
        driver.switch_to.frame("g_iframe")  # 进入新的框架
        trs = driver.find_elements_by_xpath('//tbody/tr')
        # print(trs)
        for tr in trs:  # 遍历得到歌名和id
            song_name = tr.find_element_by_xpath('.//span[@class="txt"]/a/b').get_attribute('title')
            song_id = tr.find_element_by_xpath('.//span[@class="txt"]/a').get_attribute('href')
            file_handle.write('{}  {} {}\n'.format(title, song_name, song_id))
            # 得到歌曲的id
            song_id = song_id.split('=')[-1]
            print(song_name, song_id)

            if os.path.exists(os.path.join(singer_path, (song_name + '.mp3'))):
                continue  # 如果已经存在，就继续下一首

            # 去外链地址拿到歌曲的二进制文件
            music_url = base_url + '%s' % song_id + '.mp3'
            try:  # 保存
                music = requests.get(music_url, headers=headers, timeout=20)
                with open(os.path.join(singer_path, (song_name + '.mp3')), 'wb') as file:
                    file.write(music.content)
                    print('{} Successful {}/{}.mp3'.format(count, title, song_name))
                    count += 1
            except:
                print('{} error {}/{}.mp3'.format(count, title, song_name))
            sleep(0.02)

    file_handle.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download some songs of one singer in Netease.')
    parser.add_argument("url", help="a url of a singer", type=str)
    parser.add_argument("name", help="a name of a singer", type=str)
    parser.add_argument("page", help="nums of a page", type=int)
    parser.add_argument("--path", default='', help="a path to save", type=str)
    args = parser.parse_args()

    if args.path == '':
        singer_path = './music/{}'.format(args.name)
    else:
        singer_path = args.path

    # singer_url = 'https://music.163.com/#/artist/album?id=10559'  # 歌手专辑页面
    download(args.url, args.name, page_num=args.page, singer_path=singer_path)
