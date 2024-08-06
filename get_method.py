from threading import Thread
from download_file import download
import os


def get_url(soup, page):
    data_src_dict = {}
    srcs = soup.find_all('img')
    data_src_list = [src.get('data-src') for src in srcs if src.get('data-src')]
    data_src_dict[page] = data_src_list
    return data_src_dict


def get_downurl(page, te_num, title, srcs, end_chapter):
    j = 0
    thread_list = []
    for src in srcs:
        j += 1
        t = Thread(target=download, args=(src, te_num, j, page, title), name=f'{page} + {str(j)}')
        thread_list.append(t)
        t.start()
    if page == end_chapter:
        for t in thread_list:
            t.join()  # 使主线程等待子线程运行完毕之后才退出



def get_downurl_sep(page, te_num, title, srcs, end_chapter):
    thread_list = []
    # 检查image目录是否存在,不存在则创建
    title = title+'/'+str(page)
    if not os.path.exists(title):
        os.makedirs(title)

    j = 0
    for src in srcs:
        j += 1
        t = Thread(target=download, args=(src, te_num, j, page, title), name=f'{page} + {str(j)}')
        thread_list.append(t)
        t.start()  # 调用start()方法，开始执行

    if page == end_chapter:
        for t in thread_list:
            t.join()  # 使主线程等待子线程运行完毕之后才退出



def get_page(srcs):
    temp = 0
    temp_list = list()
    for src in srcs:
        data_src = src.get('href')
        if 'comic' in data_src:
            temp_list.append('https://www.mangacopy.com' + data_src)
            temp += 1
    return temp, temp_list


def get_valid(start_chapter, end_chapter, max_chapter):
    if 1 <= start_chapter <= end_chapter <= max_chapter:
        return True
    return False