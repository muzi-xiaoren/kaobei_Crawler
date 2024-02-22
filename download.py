import os
import re
import requests
import threading


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}


max_connections = 10  # 定义最大线程数,可根据网速修改
pool_sema = threading.BoundedSemaphore(max_connections)  # 或使用Semaphore方法


def download(src, j, page, title):
    pool_sema.acquire()  # 加锁，限制线程数
    pattern = r'\/y\/(.*?)\/'
    result1 = re.search(pattern, src)
    image_name = str(page) + '_' + str(j) + '_' + result1.group(1) + '.webp'
    image_path = os.path.join(title, image_name)

    if os.path.exists(image_path):
        print(f'{image_name} already exists.', end='  ')
        pool_sema.release()  # 解锁
        return

    print(f'{image_name} is downloading', end='  ')

    response = requests.get(src, headers)
    # print(response.status_code, end=' ')
    while response.status_code != 200:
        response = requests.get(src, headers)
        # print(response.status_code)
    with open(os.path.join(title, image_name), 'wb') as f:
        f.write(response.content)
    pool_sema.release()  # 解锁
