import requests
from bs4 import BeautifulSoup
import os
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"
}


def download(response):
    data = BeautifulSoup(response.text, "lxml")
    ul_list = data.find_all(class_="photo-list-padding")

    for ul in ul_list:

        # 基础路径
        path = "./图库"
        # 解析
        li = BeautifulSoup(str(ul), "lxml")

        # 详情页网址
        page_url = "http://desk.zol.com.cn" + li.find(class_="pic")["href"]

        # 图片系列名称
        name = li.find("em").text
        # 拼接保存路径（根据图片系列不同，分类保存）
        path = path + "/" + name

        # 如果不存在就创建该文件夹
        if not os.path.exists(path):
            os.makedirs(path)

        # 详情页请求
        page_response = requests.get(url=page_url, headers=headers)
        # 设置页面编码
        page_response.encoding = "GB2312"
        page_data = BeautifulSoup(page_response.text, "lxml")

        li_list = page_data.find(class_="photo-list-box").find_all("li")
        i = 0
        for page_li in li_list:
            i += 1
            image = BeautifulSoup(str(page_li), "lxml")
            if i > 4:
                img_url = image.find("img")["srcs"]
            else:
                img_url = image.find("img")["src"]

            # 替换掉144x90的分辨率，以1920x1080分辨率保
            image_url = img_url.replace("144x90", "1920x1080")

            print(image_url)
            # 发起图片请求，content返回的是bytes，二级制型的数据。
            res = requests.get(url=image_url, headers=headers).content

            # 图片保存
            with open(path + "/" + str(i) + ".jpg", 'wb')as f:  # 以wb方式打开文件,b就是binary的缩写,代表二进制
                f.write(res)
        print("+" * 40)



if __name__ == "__main__":
    # for i in range(3):
    i = 0
    start = time.time()
    url = "http://desk.zol.com.cn/pc/"+str(i + 1)+".html"

    response = requests.get(url=url, headers=headers)
    response.encoding = "GB2312"
    download(response)

    end = time.time()
    print(end-start)


