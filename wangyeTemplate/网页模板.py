import requests
from lxml import etree
import os


def DownRar(down_url,name):
    rar_data = requests.get(url=down_url, headers=headers, stream=True)
    rar_path = 'rarList/' + name
    if rar_data.status_code == 200:
        with open(rar_path + ".rar", 'wb') as f:
            f.write(rar_data.content)
            print("ok")


def AnalysisRar(page_text):
    # 创建文件夹
    if not os.path.exists('./rarList'):
        os.mkdir('./rarList')

    # 数据解析
    tree = etree.HTML(page_text)
    a_list = tree.xpath("//div[@id='container']//div/a/@href")
    for a_li in a_list:
        # 请求地址
        moban_data = requests.get(url=a_li, headers=headers)
        moban_data.encoding = "utf-8"

        tree2 = etree.HTML(moban_data.text)
        rar_down = tree2.xpath("//div[@class='downbody']//div[@class='dian'][2]/a[1]/@href")
        rar_name = tree2.xpath("//div[@class='text_wrap']/h2/a/text()")[0]
        for rar in rar_down:
            DownRar(rar, rar_name)


if __name__ == "__main__":


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
    }
    for i in range(1,11):
        if i == 1:
            url = "http://sc.chinaz.com/moban/index.html"
        else:
            url = "http://sc.chinaz.com/moban/index_" + str(i) + ".html"
        print(url)
        response = requests.get(url=url,headers=headers)
        response.encoding = "utf-8"
        page_text = response.text
        # 解析详情网页
        AnalysisRar(page_text)