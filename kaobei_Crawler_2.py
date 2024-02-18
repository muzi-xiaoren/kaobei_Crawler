import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from get import *
import os


def down(src, count, title, mode):
    driver.get(src)
    time.sleep(1)
    for i in range(count):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
        time.sleep(0.1)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    temp_tr = soup.find('span', class_='comicCount')
    if int(mode):
        temp = get_downurl_sep(soup, page, title)
    else:
        temp = get_downurl(soup, page, title)
    print(int(temp_tr.text), temp)
    if int(temp_tr.text) == temp:
        success.add(page)
        print(f'章{page} success {success}')
        print()
    else:
        print(f'章{page} failed')
        print()
        down(src, count * 2, title, mode)


if __name__ == "__main__":
    mode = input('''请输入下载的模式:
0->全部下载在同一文件夹内
1->分文件夹进行下载
    ''') or 0
    # 初始化
    chrome_options = Options()
    # 打开终端输入    Chrome --remote-debugging-port=9222
    # 前面的chrome换成你使用的浏览器比如edge浏览器是msedge，下面Chrome需改成Edge。其他的浏览器建议自己查找，或者使用另一个方法。
    chrome_options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.mangacopy.com/comic/tiancaimonvmeimole")  # 此处修改页面url
    except TimeoutException:
        driver.execute_script('window.stop()')

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
    success = set()
    page = 0

    for src in src_list:
        count = 4
        page += 1
        down(src, count, title, mode)

    driver.quit()
    print(f"页面读取{page_all}章，总共下载{page}章")
    exit()
