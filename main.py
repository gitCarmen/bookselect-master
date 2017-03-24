from multiprocessing import Pool
from channel_extract import channel_list
from books import book_list
from chapters import get_chapter_list,chapter_list

#
#
# def get_all_links_from(channel):
#
#     for i in range(1,10):
#         get_links_from(channel,i)
#
#
# if __name__ == '__main__':
#     # pool = Pool()
#     # pool = Pool(processes=6)
#     # pool.map(get_all_links_from,'http://www.tsxsw.com/fenlei1/')
#     # pool = Pool()
#     # pool = Pool(processes=6)
#     for i in range(0, len(channel_list)):
#     # for i in len(channel_list):
#     #     pool.map(get_all_links_from, channel_list[i])
#         get_all_links_from(channel_list[i])
#
#     # get_all_links_from('fenlei7')

# ================================================= < <链接去重 > > =====================================================

# 设计思路：
# 1.分两个数据库，第一个用于只用于存放抓取下来的 url (ulr_list)；第二个则储存 url 对应的物品详情信息(item_info)
# 2.在抓取过程中在第二个数据库中写入数据的同时，新增一个字段(key) 'index_url' 即该详情对应的链接
# 3.若抓取中断，在第二个存放详情页信息的数据库中的 url 字段应该是第一个数据库中 url 集合的子集
# 4.两个集合的 url 相减得出圣贤应该抓取的 url 还有哪些


db_urls = [item['link'] for item in book_list.find()]     # 用列表解析式装入所有要爬取的链接
index_urls = [item['book_link'] for item in chapter_list.find()] # 所引出详情信息数据库中所有的现存的 url 字段
x = set(db_urls)                                        # 转换成集合的数据结构
y = set(index_urls)
rest_of_urls = x-y                                      # 相减

# ======================================================================================================================

if __name__ == '__main__':

    pool = Pool()

    pool.map(get_chapter_list,rest_of_urls)



