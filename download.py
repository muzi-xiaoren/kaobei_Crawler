import os
import requests


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}


def download(src, j, page):
    image_name = str(page) + '_' + str(j) + '_' + src[72:85] + '.webp'
    image_path = os.path.join('kaobei_images', image_name)

    if os.path.exists(image_path):
        print(f'{image_name} already exists.', end='  ')
        return

    print(f'{image_name} is downloading', end='  ')

    response = requests.get(src, headers)
    # print(response.status_code, end=' ')
    while response.status_code != 200:
        response = requests.get(src, headers)
        # print(response.status_code)
    with open(os.path.join('kaobei_images', image_name), 'wb') as f:
        f.write(response.content)
