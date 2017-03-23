from multiprocessing import Pool
# from channel_extract import channel_list
from books import get_links_from




def get_all_links_from(channel):

    for i in range(1,30):
        get_links_from(channel,i)


if __name__ == '__main__':
    # pool = Pool()
    # pool = Pool(processes=6)
    # pool.map(get_all_links_from,'http://www.tsxsw.com/fenlei1/')
    get_all_links_from('fenlei7')
