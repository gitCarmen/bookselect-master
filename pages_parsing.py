#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import pymongo
import requests
from bs4 import BeautifulSoup
import urllib
# from collections import OrderedDict
url_host = 'http://www.tsxsw.com/'

client = pymongo.MongoClient('localhost', 27017)
books = client['books']
book_list = books['book_list']
chapter_list = books['chapter_list']

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
#spider1 get all links of fictions
def get_links_from(channel, pages):

    list_view = '{}{}/{}/'.format(url_host,channel,pages)
    user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
    headers={'User_Agent':user_agent}
    request = urllib.request.Request(list_view, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    soup=BeautifulSoup(html,"html5lib")
    imgs = soup.select('div.w.aw.main > div.listcon > ul > li.one > div.img > h1 > a > img')

    titles=soup.select('div.w.aw.main > div.listcon > ul > li.one > div.art > h1 > a')
    authors= soup.select('div.w.aw.main > div.listcon > ul > li.one > div.art > author ')
    lastchapters= soup.select('div.w.aw.main > div.listcon > ul > li.one > div.art > lastchapter')
    # print(titles)
    for title,img,author,lastchapter  in zip(titles,imgs,authors,lastchapters):
            data ={
                'title': title.get_text(),
                # 'link': title.get('href'),
                # 'cate':cate_list[channel],
                # 'img':img.get('src'),
                # 'author':author.get_text()[0],
                # 'state': author.get_text()[1],
                # 'lastchapter':lastchapter.get_text(),
                # 'no':title.get('href').split('/')[-2]
            }
            print(data)


# spider2
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
    chapters_list=[title,author]
    num=0
    for chapter in chapters:
        data={
            'chapter_name': chapter.get_text(),
            'chapter_link':url + chapter.get('href'),
            'book_title':title,
            'author':author,
            'cate':cate,
            # 'chapter_no':num+1

        }
    #
    #     get_chapter_detail(data['chapter_link'],data['book_title'],data['chapter_name'])
        print(data)
        chapter_list.insert(data)



#spider3
def get_chapter_detail(url,book_name,chapter_name):
    user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
    headers={'User_Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    soup=BeautifulSoup(html,"lxml")
    txt=soup.find_all('dd',id="contents")    #用bs搜索
    filename=book_name + '-' + chapter_name+'.txt'
    with open(filename,'a+') as f:

        for item in txt:
        #     print(item.get_text('\n''\n', strip=True))
            f.write(item.get_text('\n''\n', strip=True))

            # print(p)
    f.close()
    print('ok')
    time.sleep(3)

# get_chapter_detail('http://www.tsxsw.com/html/1/1455/780301.html','道神','第一卷 雏鹰展翅 第1章 一人一剑，杀上九重天@')

get_chapter_list('http://www.tsxsw.com/html/33/33254/')
# get_links_from('fenlei1', '2')