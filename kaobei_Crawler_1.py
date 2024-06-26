from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from get import *
import os
import time

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
''') or 1
    # 初始化
    options = Options()
    options.add_argument("window-position=660,0")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.mangacopy.com/web/login/loginByAccount?url=person%2Fhome')
    except TimeoutException:
        driver.execute_script('window.stop()')

    time.sleep(1)
    # 查找用户名、密码输入框并输入
    driver.find_element(By.XPATH, '//*[@id="pane-login"]/form/div[1]/div/div[1]/input').send_keys('test_345')
    driver.find_element(By.XPATH, '//*[@id="pane-login"]/form/div[2]/div/div/input').send_keys('123456789')
    # 点击登录按钮
    element = driver.find_element(By.CLASS_NAME, "el-button--danger")
    driver.execute_script("arguments[0].click()", element)
    time.sleep(1)
    print("访问拷贝页面中,.....")
    driver.get("https://www.mangacopy.com/comic/shejianshangdedixiacheng#")  # 此处修改页面url
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