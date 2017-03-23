from bs4 import BeautifulSoup
import requests
import urllib

start_url = 'http://book.easou.com/w/list/yanqing_3.html'
url_host = 'http://www.tsxsw.com/'

def get_index_url(url):
    # url = start_url
    user_agent='Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
    headers={'User_Agent':user_agent}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    html = response.read()
    # wb_data = requests.get(url)
    soup = BeautifulSoup(html, 'html5lib')
    links = soup.select('body > div.main.m_menu > ul > li > a')
    # print(links)
    channel_list=[]
    for link in links:
        channel_list.append(link.get('href'))
    #     data={
    #         'cate_name': link.get_text(),
    #         'cate_url':  link.get('href')
    #     }
    #     # cate_name= link.get_text()
    #     # cate_url = link.get('href')
    #     # print(data)
    #     channel_list.append(data)
    # # print(channel_list)
    return(channel_list)

# get_index_url(start_url)

# channel_list = '''
#     http://www.tsxsw.com/fenlei1/
#     http://www.tsxsw.com/fenlei2/
#     http://www.tsxsw.com/fenlei3/
#     http://www.tsxsw.com/fenlei4/
#     http://www.tsxsw.com/fenlei5/
#     http://www.tsxsw.com/fenlei6/
#     http://www.tsxsw.com/fenlei7/
#     http://www.tsxsw.com/qb/
# '''
channel_list = get_index_url(url_host)[1:-1]
print(channel_list)