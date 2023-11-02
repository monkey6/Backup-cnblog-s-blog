import json
import re
import requests
import os
import time
import random


# 下载图片，并保存到本地
def download_img(img_address, local_address):
    if not os.path.exists(local_address):
        os.mkdir(local_address)
    image_filename = os.path.basename(img_address)
    image_filename_with_dir = f'{local_address}/{image_filename}'
    response = requests.get(img_address)
    if response.status_code == 200:
        with open(image_filename_with_dir, 'wb') as f:
            f.write(response.content)
    else:
        print(f'\033[33m{img_address, local_address}\033[0m')
    return image_filename_with_dir


# 替换网上的图片
def replace_blog_img(blog_content, local_address):
    pattern = r'!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, blog_content)
    for img in matches:
        blog_content = blog_content.replace(img, download_img(img, local_address))
        time.sleep(random.randint(1, 3))
    return blog_content


def main():
    # 将json解析出来，解析出来是list类型
    with open('posts.json', mode='rt', encoding='utf-8') as fp:
        blog_list = json.load(fp)

    for blog in blog_list:
        title = blog['Title'].replace('/', '_')
        if blog['IsMarkdown']:
            with open(f'{title}.md', mode='wt', encoding='utf-8') as fp:
                fp.write(replace_blog_img(blog['Body'], title))
            time.sleep(2)
            print(f'{title}已经解析OK！')
    print('已全部解析完成！')


def test():
    with open('posts.json', mode='rt', encoding='utf-8') as fp:
        blog_list = json.load(fp)

    blog = blog_list[1]
    title = blog['Title'].replace('/', '_')
    if blog['IsMarkdown']:
        with open(f'{title}.md', mode='wt', encoding='utf-8') as fp:
            fp.write(replace_blog_img(blog['Body'], title))


if __name__ == '__main__':
    main()
