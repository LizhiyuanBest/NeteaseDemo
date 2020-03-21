# -*- coding=utf-8 -*

# # 导入框架
# import requests
#
# # 确定url
# url ='https://m10.music.126.net/20200320105705/c184de11cedda20591a36a43deae120c/yyaac/015c/5609/0159/66a937cca3acbb5f0df4639aa2657946.m4a'
#
# # 请求
# result = requests.get(url).content
#
# with open('./a.m4a', 'wb') as f:
#     f.write(result)

# 0.导入框架
import requests
from lxml import etree

# 1.确定url
url = 'https://music.163.com/playlist?id=2153548870'
# 5.拿到外链
base_url = 'https://link.hhtjim.com/163/'
# 2.请求
result = requests.get(url).text
print(result)

# 3.筛选数据
dom = etree.HTML(result)
ids = dom.xpath('//a[contains(@href,"song?")]/@href')
print(ids)

# 4.遍历
for song_id in ids:
    # 过滤切割
    count_id = song_id.strip('/song?id=')
    print(count_id)

    music_url = base_url + '%s' % count_id + '.mp3'

    music = requests.get(music_url).content

    # 保存
    with open('./Music/%s.mp3' % count_id, 'wb') as file:
        file.write(music)
