from selenium import webdriver
import os
import time
import html2text as ht
from bs4 import BeautifulSoup
import parsel
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions



html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {content}
</body>
</html>"""

path = "./文件"

def init():
    # 实现无可视化界面得操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 实施规避检测
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(chrome_options=chrome_options,options=option)

    driver.get("https://www.csdn.net/")
    time.sleep(0.5)

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    for y in range(10):
        js = 'window.scrollBy(0,200)'
        driver.execute_script(js)
        time.sleep(0.5)

    time.sleep(3)
    return driver


def Crawling(driver):
    data = BeautifulSoup(driver.page_source, "lxml")

    li_list = data.find(class_="feedlist_mod home").find_all(class_="clearfix")
    for li in li_list:
        li_data = BeautifulSoup(str(li), "lxml")
        try:
            # 详情页url
            page_url = li_data.find("a")["href"]
        except:
            continue

        # 如果是官方直播就跳过
        if li_data.find(class_="name").find("a").text.strip() == '官方直播':
            continue
        # 文章标题
        title = li_data.find("a").text.replace(" ", "")
        page_Crawling(title,page_url,driver)


def page_Crawling(title,page_url,driver):
    # 如果不存在就创建该文件夹
    if not os.path.exists(path):
        os.makedirs(path)

    driver.get(page_url)
    # page_data = BeautifulSoup(driver.page_source, "lxml")

    # text = page_data.find(class_="article_content clearfix")
    selector = parsel.Selector(driver.page_source)
    text = selector.css("article").get()
    with open("text.html", "w", encoding="utf-8") as f:
        f.write(html.format(content=text))

    text_maker = ht.HTML2Text()
    # 读取html格式文件
    with open('text.html', 'r', encoding='UTF-8') as f:
        htmlpage = f.read()
    # 处理html格式文件中的内容
    text = text_maker.handle(htmlpage)
    # 写入处理后的内容
    with open(path + "/" + title + '.md', 'w', encoding="utf-8") as f:
        f.write(text)
    print(title + "爬取完毕")





if __name__ == "__main__":
    driver = init()
    Crawling(driver)
