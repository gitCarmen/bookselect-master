import time
import pymongo
import requests
from bs4 import BeautifulSoup
import urllib
# from collections import OrderedDict

client = pymongo.MongoClient('localhost', 27017)
tsxsw = client['tsxsw']
book_list = tsxsw['book_list']
chapter_list = tsxsw['chapter_list']




url_host = 'http://www.tsxsw.com/'
cate_list={
    'fenlei1':'玄幻小说',
    'fenlei2':'仙侠小说',
    'fenlei3':'都市小说',
    'fenlei4':'历史小说',
    'fenlei5':'网游小说',
    'fenlei6':'恐怖小说',
    'fenlei7':'其他小说',
    'qb':'全本'
}
def get_links_from(channel, pages):

    url = '{}{}/{}/'.format(url_host,channel,pages)
    # 请求列表页面地址
    wb_data= requests.get(url)
    wb_data.encoding='gbk'

    # wb_data.encoding = 'gb18030'
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    # user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
    # headers={'User_Agent':user_agent}
    # request = urllib.request.Request(url, headers=headers)
    # response = urllib.request.urlopen(request)
    # html = response.read()
    # time.sleep(1)
    # soup=BeautifulSoup(html,"html.parser")

    books=soup.select('div.w.aw.main > div.listcon > ul > li.one ')
    imgs = soup.select('div.w.aw.main > div.listcon > ul > li.one > div.img > h1 > a > img')
    titles=soup.select('div.w.aw.main > div.listcon > ul > li.one > div.art > h1 > a')
    authors= soup.select('div.w.aw.main > div.listcon > ul > li.one > div.art > p.author  ')
    lastchapters= soup.select('div.w.aw.main > div.listcon > ul > li.one > div.art > p.lastchapter > a')

    for i in range(len(books)):
        data ={
            'title': titles[i].text,
            'link':titles[i].get('href'),
            'cate':cate_list[channel],
            'cate_no':channel[-1],
            'img':imgs[i].get('src'),
            'author':authors[i].get_text().split('\xa0\xa0\xa0\xa0')[0],
            'state': authors[i].get_text().split('\xa0\xa0\xa0\xa0')[-1],
            'lastchapter':lastchapters[i].get_text(),
            'no':titles[i].get('href').split('/')[-2]

        }
        print(data)
        book_list.insert(data)


# for i in range(1, 10):
#     get_links_from('fenlei7', i)
# get_links_from('fenlei1', '400')