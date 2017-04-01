import time
import pymongo
import requests
from bs4 import BeautifulSoup
import re
# from collections import OrderedDict

client = pymongo.MongoClient('localhost', 27017)
tsxsw = client['tsxsw']
book_list = tsxsw['book_list']
chapter_list = tsxsw['chapter_list']

heads = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}
#===========================设置自动代理===============================
class MyProxy(object):
    def __init__(self):
        self.proxy_list = []
        self.refresh_ip_list()
        self.__next__()

    def refresh_ip_list(self):
        print("Refreshing MyProxy IP List...")
        soup = get_soup_from_url("http://www.xicidaili.com/nn/")

        #正则寻找IP地址
        re_ip = re.compile(
            r"(?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))")
        ip_tag = soup.find_all("td", text=re_ip)  # get_text()

        #获得IP端口
        ports = soup.select("tr > td:nth-of-type(3)")

        #获取Proxy速度
        speed_work = [i.get("class")[1] for i in soup.select("tr > td:nth-of-type(7) > div > div")]

        #获取Proxy连接速度
        speed_connect = [i.get("class")[1] for i in soup.select("tr > td:nth-of-type(8) > div > div")]

        #合并所有数据至ip_data : {"ip":XX.XX.XX.XX,"speed_work":"fast","speed_connect":"medium"}
        ip_data = []
        for ip, workspeed, connectspeed,port in zip(ip_tag, speed_work, speed_connect,ports):
            data = {
                "ip": "{ip}:{port}".format(ip = ip.get_text(),port = port.get_text()),
                "speed_work": workspeed,
                "speed_connect": connectspeed
            }
            ip_data.append(data)

        #筛选出速度快的Proxy
        ip_data_filtered = list(filter(lambda i: i["speed_work"] == "fast" and i["speed_connect"] == "fast", ip_data))
        self.proxy_list = [i["ip"] for i in ip_data_filtered]
        self.proxy_list = iter(self.proxy_list)

    def __iter__(self):
        return self

    def __next__(self):
        print("Switching IP Address...")
        try:
            self.currentIP = next(self.proxy_list)
            print("New Proxy: %s" % (self.currentIP))
            return self.currentIP
        except StopIteration as e:
            self.refresh_ip_list()
            return self.__next__()

    def get_current_proxy(self):
        return {"http": self.currentIP}

    def get_next_proxy(self):
        return {"http": self.__next__()}


#==================================根据自动代理取得soup============
def get_soup_from_url(url,auto_proxy = False,coding='gbk'):
    if auto_proxy:
        # proxy = my_proxy.get_current_proxy()
        proxy = my_proxy.get_current_proxy()
    else:
        proxy = {}

    while True:
        # if proxy: print("Trying Proxy:%s" % proxy["http"])
        try:
            respond = requests.get(url,headers=heads,proxies = proxy,timeout=8)
            respond.encoding = coding
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print("Proxy %s isn't working well..." % proxy["http"])
            proxy = my_proxy.get_next_proxy()
        else:
            if respond.status_code!= 200:
                print("respond status code problem: %s" % respond.status_code)
                proxy = my_proxy.get_next_proxy()
                continue
            break

    soup = BeautifulSoup(respond.text,'lxml')
    print(soup)
    return soup
#==============================================================================================

def get_chapter_list(url):
	# 请求目录页面地址
    # wb_data = requests.get(url)

    # 延时一秒钟，太快容易被封IP
    time.sleep(1)

    # 开始解析网页数据

    time.sleep(1)
    soup = get_soup_from_url(url, True,'gbk')
    # 鼠标放到标题上，右键，审查元素，再右键，提取Css Path
    title = soup.title.text.split('/')[0]
    detail= soup.select(' div.article > p.author > span')
    author =detail[1].text

    cate =detail[0].text
    state=detail[2].text
    update=detail[3].text
    chapters = soup.select('ul.chapters > li > a ')


    for i,  chapter in enumerate (chapters):
        data={
            'chapter_name': chapter.get_text(),
            'chapter_link':url + chapter.get('href'),
            'book_title':title,
            'author':author,
            'cate':cate,
            'chapter_id':i+1,
            'book_link':url,
            # 'chapter_no':num+1

        }
    #
    #     get_chapter_detail(data['chapter_link'],data['book_title'],data['chapter_name'])
        print(data)
        chapter_list.insert(data)


#===================================测试本页==================================
my_proxy = MyProxy()
get_chapter_list('http://www.tsxsw.com/html/34/34622/')
