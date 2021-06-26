from selenium import webdriver
import time
import os
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup

path = "./网易新闻"


# 初始化
def init():
    # 实现无可视化界面得操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 设置chrome_options=chrome_options即可实现无界面
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver = webdriver.Chrome()
    # 把浏览器实现全屏
    # driver.maximize_window()
    # 返回driver
    return driver


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41"
}


# 获取模块URL
def getUrl(driver):
    url = "https://news.163.com/"
    driver.get(url)
    response = driver.page_source
    # 目标标题索引 （2:国内，3:国际，5:军事）
    target_list = [2, 3, 5]
    data = BeautifulSoup(response, "html.parser")
    li_list = data.find(class_="ns_area list").find_all("li")
    for index in target_list:
        url = li_list[index].find("a")["href"]
        title = li_list[index].find("a").text
        # 如果模块文件埃及不存在就要创建
        if not os.path.exists(path):
            os.mkdir(path)
        model_path = path + "/" + str(title)
        # 如果模块文件不存在就要创建
        if not os.path.exists(model_path):
            os.mkdir(model_path)
        parse_model(driver, url, model_path)


# 获取模块页面URL
def parse_model(driver, url, model_path):
    driver.get(url)
    model_response = driver.page_source
    model_data = BeautifulSoup(model_response, "html.parser")
    div_list = model_data.find(class_="ndi_main").find_all(class_="news_title")
    for i in div_list:
        # if i.find("a") is not None and i.find("a").find("img") is not None:
        detail_url = i.find("a")["href"]
        parse_detail(detail_url, model_path)


# 爬取详情页
def parse_detail(detail_url, model_path):
    detail_response = requests.get(url=detail_url, headers=headers).text
    detail_data = BeautifulSoup(detail_response, "html.parser")
    if detail_data.find(class_="post_title") is None:
        return
    #文章标题
    title = detail_data.find(class_="post_title").text
    title = replaceTitle(title)
    body = detail_data.find(class_="post_body").find_all("p")
    print("正在保存：" + title)
    try:
        with open(model_path + "/" + title + ".txt", "w", encoding="utf-8") as f:
            for i in body:
                f.write(str(i.text.strip()) + "\n")
        f.close()
    except:
        os.remove(model_path + "/" + title + ".txt")


symbol_list = ["\\", "/", "<", ":", "*", "?", "<", ">", "|","\""]

def replaceTitle(title):
    for i in symbol_list:
        if title.find(str(i)) != -1:
            print(title)
            title = title.replace(str(i),"")

    return title


if __name__ == '__main__':
    driver = init()
    getUrl(driver)
