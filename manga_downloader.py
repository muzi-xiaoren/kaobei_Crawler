from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from get_method import get_url, get_downurl, get_downurl_sep, get_page
import time
import os
import queue
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def initialize_driver():
    # 初始化
    options = Options()

    # 启用无头模式时开启。
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")  # 禁用GPU加速
    options.add_argument("--window-size=1920x1080")  # 设置窗口大小，防止某些元素不可见

    # # 不启用无头模式时开启，调式代码或者看报错的时候使用。
    # options.add_argument("window-position=660,0")

    driver = webdriver.Chrome(options=options)
    return driver


def login(driver, username, password):
    try:
        driver.get('https://www.mangacopy.com/web/login/loginByAccount?url=person%2Fhome')
    except TimeoutException:
        driver.execute_script('window.stop()')

    time.sleep(1)
    # 查找用户名、密码输入框并输入
    driver.find_element(By.XPATH, '//*[@id="pane-login"]/form/div[1]/div/div[1]/input').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="pane-login"]/form/div[2]/div/div/input').send_keys(password)
    # 点击登录按钮
    element = driver.find_element(By.CLASS_NAME, "el-button--danger")
    driver.execute_script("arguments[0].click()", element)
    time.sleep(1)


def get_comic_info(driver, url):
    print("访问拷贝页面中,.....")
    driver.get(url)  # 此处修改页面url
    time.sleep(1)
    html = driver.page_source  # 获取当前页面HTML
    soup = BeautifulSoup(html, "html.parser")  # 用BeautifulSoup解析
    title = soup.find('h6').text
    # 检查image目录是否存在,不存在则创建
    if not os.path.exists(title):
        os.makedirs(title)
    soup = soup.find(name='div', attrs={"id": "default全部"})  # print(srcs, len(srcs), sep='/n')    # 查找元素等操作show
    srcs = soup.find_all('a')
    page_all, src_list = get_page(srcs)
    return title, page_all, src_list


def url_producer(driver, src, count, title, page, q_list):
    # print(f"Producer thread for page {page} started.")
    driver.get(src)
    time.sleep(1)
    for _ in range(count):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(0.1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    temp_tr = soup.find('span', class_='comicCount')
    temp = get_url(soup, page)
    print()
    print(int(temp_tr.text), len(temp[page]))
    if int(temp_tr.text) == len(temp[page]):
        q_list.put(temp)
    else:
        url_producer(driver, src, count * 2, title, page, q_list)
    # print(f"Producer thread for page {page} finished.")


def url_consumer(title, mode, q_list, end_chapter):
    # print("Consumer thread started.")
    while True:
        item = q_list.get()
        if item is None:
            break

        for page, data_src_list in item.items():
            te_num = len(data_src_list)
            if int(mode):
                get_downurl_sep(page, te_num, title, data_src_list, end_chapter)
            else:
                get_downurl(page, te_num, title, data_src_list, end_chapter)
        q_list.task_done()
    # print("Consumer thread finished.")


def start_threads(driver, src_list, start_chapter, end_chapter, title, mode):
    page = start_chapter - 1
    q_list = queue.Queue()
    
    # 启动消费者线程
    consumer_thread = Thread(target=url_consumer, args=(title, mode, q_list, end_chapter))
    consumer_thread.start()

    # 启动生产者线程
    for i in range(start_chapter - 1, end_chapter):
        src = src_list[i]
        count = 4
        page += 1
        t = Thread(target=url_producer, args=(driver, src, count, title, page, q_list))
        t.start()
        t.join()  # 等待当前线程完成再启动下一个

    # 等待所有生产者线程完成
    q_list.join()

    # 停止消费者线程
    q_list.put(None)
    consumer_thread.join()