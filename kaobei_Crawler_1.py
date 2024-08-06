from manga_downloader import initialize_driver, login, get_comic_info, start_threads
from get_method import get_valid


if __name__ == "__main__":
    mode = input('''请输入下载的模式(回车默认分文件夹下载):
0->全部下载在同一文件夹内
1->分文件夹进行下载
''') or 1

    # 获取用户输入的章节范围
    chapter_range = input(f'''请输入要下载的章节范围(例如 3-15)，回车默认全部下载: 
''') or f"1-114514"
    start_chapter, end_chapter = map(int, chapter_range.split('-'))

    driver = initialize_driver()
    login(driver, 'test_345', '123456789')

    title, page_all, src_list = get_comic_info(driver, "https://www.mangacopy.com/comic/sydsz")

    if end_chapter == 114514:
        end_chapter = page_all

    while not get_valid(start_chapter, end_chapter, page_all):
        chapter_range = input(f'''输入不合法，请输入一个有效的章节范围（例如 1-{page_all}（本篇总章数））
''') or f"1-{page_all}"
        start_chapter, end_chapter = map(int, chapter_range.split('-'))

    start_threads(driver, src_list, start_chapter, end_chapter, title, mode)

    driver.quit()
    print(f"页面读取{page_all}章，总共下载{end_chapter - start_chapter + 1}章")
