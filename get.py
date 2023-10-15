from threading import Thread
from download import *
import threading

Lock = threading.Lock()


def get_downurl(soup, page):
    j = 0
    srcs = soup.find_all('img')
    for src in srcs:
        temp = src.get('data-src')
        if temp:
            Lock.acquire()
            j += 1
            t = Thread(target=download, args=(temp, j, page), name=f'{page} + {str(j)}')
            t.start()
            Lock.release()
    return j


def get_page(srcs):
    temp = 0
    temp_list = list()
    for src in srcs:
        data_src = src.get('href')
        if 'comic' in data_src:
            temp_list.append('https://www.mangacopy.com' + data_src)
            temp += 1
    return temp, temp_list
