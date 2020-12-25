import requests
from bs4 import BeautifulSoup
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}



def download(path,data):
    ul = data.find(class_="slist").find_all("li")

    for li in ul:
        li_data = BeautifulSoup(str(li), "html.parser")
        page_url = "http://pic.netbian.com/" + li_data.find("a")['href']
        title = li_data.find("img")['alt']

        page_data = requests.get(url=page_url, headers=headers)
        response_data = BeautifulSoup(page_data.text, "html.parser")
        img_url = "http://pic.netbian.com" + response_data.find(class_="photo-pic").find("img")['src']

        img_res = requests.get(url=img_url, headers=headers).content

        with open(path + "/" + title + ".jpg", "wb") as f:
            print("正在保存："+title)
            f.write(img_res)

if __name__ == '__main__':
    path = "./图片"
    if not os.path.exists(path):
        os.mkdir(path)

    for i in range(1,4):
        data_path = path + "/" + str(i)
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        if i == 1:
            url = "http://pic.netbian.com/index.html"
        else:
            url = "http://pic.netbian.com/index_"+str(i)+".html"
        response = requests.get(url=url, headers=headers)
        response.encoding = 'gbk'
        data = BeautifulSoup(response.text, "html.parser")
        download(data_path,data)