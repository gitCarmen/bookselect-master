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




def get_chapter_list(url):
	# 请求目录页面地址
    # wb_data = requests.get(url)

    # 延时一秒钟，太快容易被封IP
    time.sleep(1)

    # 开始解析网页数据
    user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
    headers={'User_Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    soup=BeautifulSoup(html,"lxml")

    # 鼠标放到标题上，右键，审查元素，再右键，提取Css Path
    title = soup.title.text.split('/')[0]
    columns =soup.select('tr ')
    detail= soup.select(' div.article > p.author > span')
    author =detail[1].text

    cate =detail[0].text
    state=detail[2].text
    update=detail[3].text

    # print(str(columns[2]).split('href='))
    # soup2 = BeautifulSoup(columns[1],'lxml')
    # print(soup2)
    chapters = soup.select('ul.chapters > li > a ')

    num=0
    for i,  chapter in enumerate (chapters):
        data={
            'chapter_name': chapter.get_text(),
            'chapter_link':url + chapter.get('href'),
            'book_title':title,
            'author':author,
            'cate':cate,
            'chapter_id':i,

            # 'chapter_no':num+1

        }
    #
    #     get_chapter_detail(data['chapter_link'],data['book_title'],data['chapter_name'])
        print(data)
        chapter_list.insert(data)

get_chapter_list('http://www.tsxsw.com/html/33/33730/')
