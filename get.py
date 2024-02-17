import time
from threading import Thread
from download import *
import threading


max_connections = 10  # 定义最大线程数,可根据网速修改
pool_sema = threading.BoundedSemaphore(max_connections)  # 或使用Semaphore方法


def get_downurl(soup, page, title):
    j = 0
    thread_list = []
    srcs = soup.find_all('img')
    for src in srcs:
        temp = src.get('data-src')
        if temp:
            j += 1
            t = Thread(target=download, args=(temp, j, page, title), name=f'{page} + {str(j)}')
            thread_list.append(t)

    for t in thread_list:
        t.start()  # 调用start()方法，开始执行

    for t in thread_list:
        t.join()  # 子线程调用join()方法，使主线程等待子线程运行完毕之后才退出

    return j


def get_downurl_sep(soup, page, title):
    thread_list = []
    # 检查image目录是否存在,不存在则创建
    title = title+'/'+str(page)
    if not os.path.exists(title):
        os.makedirs(title)

    j = 0
    srcs = soup.find_all('img')
    for src in srcs:
        temp = src.get('data-src')
        if temp:
            j += 1
            t = Thread(target=download, args=(temp, j, page, title), name=f'{page} + {str(j)}')
            thread_list.append(t)

    for t in thread_list:
        t.start()  # 调用start()方法，开始执行

    for t in thread_list:
        t.join()  # 子线程调用join()方法，使主线程等待子线程运行完毕之后才退出

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
