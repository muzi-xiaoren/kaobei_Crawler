import threading
import time
import requests
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from threading import Thread
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import os


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
Lock = threading.Lock()


def download(src, j, page):
    image_name = str(page) + '_' + str(j) + '_' + src[72:85] + '.webp'
    image_path = os.path.join('kaobei_images', image_name)

    if os.path.exists(image_path):
        print(f'{image_name} already exists.', end='  ')
        return

    print(f'{image_name} is downloading', end='  ')

    response = requests.get(src, headers)
    print(response.status_code, end=' ')
    while response.status_code != 200:
        response = requests.get(src, headers)
        print(response.status_code)
    with open(os.path.join('kaobei_images', image_name), 'wb') as f:
        f.write(response.content)


def write_to_file(filename, variable):
    with open(filename, 'w') as file:
        file.write(str(variable))


def read_from_file(filename):
    with open(filename, 'r') as file:
        data = eval(file.read())
        success = data['success']
        failed = data['failed']
        return success, failed


def get_url(soup, page):
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


def main():
    # 初始化
    driver = webdriver.Chrome()

    try:
        driver.get('https://www.mangacopy.com/web/login/loginByAccount?url=person%2Fhome')
    except TimeoutException:
        driver.execute_script('window.stop()')

    time.sleep(1)
    # 查找用户名、密码输入框并输入
    driver.find_element(By.XPATH, '//*[@id="pane-login"]/form/div[1]/div/div[1]/input').send_keys('saving_')
    driver.find_element(By.XPATH, '//*[@id="pane-login"]/form/div[2]/div/div/input').send_keys('345ldl!?')
    # 点击登录按钮
    element = driver.find_element(By.CLASS_NAME, "el-button--danger")
    driver.execute_script("arguments[0].click()", element)
    time.sleep(1)
    print("访问拷贝页面中,.....")
    driver.get("https://www.mangacopy.com/comic/womengshoujilexingfudelianai")  # 此处修改页面url
    time.sleep(1)
    html = driver.page_source  # 获取当前页面HTML
    soup = BeautifulSoup(html, "html.parser")  # 用BeautifulSoup解析
    soup = soup.find(name='div', attrs={"id": "default全部"})  # print(srcs, len(srcs), sep='/n')    # 查找元素等操作show
    srcs = soup.find_all('a')
    page = 0
    success, failed = read_from_file('data.txt')
    for src in srcs:
        page += 1
        data_src = src.get('href')  # print(data_src)
        if page not in success and 'comic' in data_src:
            data_src = 'https://www.mangacopy.com' + data_src
            driver.get(data_src)
            time.sleep(1)
            for i in range(3):
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.SPACE)
                time.sleep(0.2)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            temp_tr = soup.find('span', class_='comicCount')
            temp = get_url(soup, page)
            print(int(temp_tr.text), temp)
            if int(temp_tr.text) == temp:
                success.add(page)
                failed.remove(page)
                write_to_file('data.txt', {'success': success, 'failed': failed})
                print()
                print(f'章{page} download successfully       {success}')
            else:
                print()
                print(f'章{page} download failed')
    driver.quit()
    print(f"总共下载{page}章")


# 检查image目录是否存在,不存在则创建
if not os.path.exists('kaobei_images'):
    os.makedirs('kaobei_images')

success, failed = read_from_file('data.txt')

while len(failed) != 0:
    try:
        main()
        success, failed = read_from_file('data.txt')
        if len(failed) == 0:
            break
    except Exception as e:
        print(f"程序执行失败: {e}")
        print("等待一段时间后重新运行...")
        time.sleep(1)

''' 优化方案：
1.使用默认浏览器打开，省略登陆步骤。
2.初始化从键盘输入页面和章数(或者自动获取章数)，自动初始化success和failed数组。
3.下载failed后，进入下载并且重新下载本章，for i in range(3):使send_keys的次数翻倍，然后下载成功后重置send_keys次数
4.爬取和下载功能独立，实现边爬取边多线程下载
5.多个浏览器线程爬取页面？(暂不考虑)

'''
