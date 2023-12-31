import time
from threading import Thread
from download import *
import threading

Lock = threading.Lock()


def get_downurl(soup, page, title):
    j = 0
    srcs = soup.find_all('img')
    for src in srcs:
        temp = src.get('data-src')
        if temp:
            Lock.acquire()
            j += 1
            t = Thread(target=download, args=(temp, j, page, title), name=f'{page} + {str(j)}')
            t.start()
            Lock.release()
            time.sleep(0.05)
    # time.sleep(1)
    return j


def get_downurl_sep(soup, page, title):
    # 检查image目录是否存在,不存在则创建
    title = title+'/'+str(page)
    if not os.path.exists(title):
        os.makedirs(title)

    j = 0
    srcs = soup.find_all('img')
    for src in srcs:
        temp = src.get('data-src')
        if temp:
            Lock.acquire()
            j += 1
            t = Thread(target=download, args=(temp, j, page, title), name=f'{page} + {str(j)}')
            t.start()
            Lock.release()
            time.sleep(0.05)
    # time.sleep(1)
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
