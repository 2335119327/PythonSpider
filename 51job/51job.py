from selenium import webdriver
import time
import pymysql
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from bs4 import BeautifulSoup
from urllib import parse


num = 2
sql = "insert into 51job(id,title,company,price,education,experience, welfare,address,text) values(null,%s,%s,%s,%s,%s,%s,%s,%s)"
name = ""

#初始化浏览器
def init():
    global name
    # 实现无可视化界面得操作
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 设置chrome_options=chrome_options即可实现无界面
    driver = webdriver.Chrome(chrome_options=chrome_options)
    time.sleep(0.5)
    # 把浏览器实现全屏
    # driver.maximize_window()
    time.sleep(0.5)
    driver.get("https://search.51job.com/list/000000,000000,0000,00,9,99,"+str(name)+",2,1.html")
    source = driver.page_source
    # 返回driver
    return driver,source


#解析
def download(driver,page_text,conn,cur):
    global num
    global name
    global sql

    # 使用lxml XML解析器
    bs = BeautifulSoup(page_text, "lxml")
    div_list = bs.find(class_="j_joblist").find_all(class_="e")
    for li in div_list:
        bs = BeautifulSoup(str(li), "lxml")
        #职位名称
        title = bs.find(class_="jname at").text
        #工资
        price = bs.find(class_="sal").text
        try:
            #公司    福利
            welfare = bs.find(class_="tags")["title"]
        except:
            welfare = "无福利"
        #公司名称
        company = bs.find(class_="cname at")['title']
        #详情页URL
        url = bs.find(class_="el")['href']
        #经验
        experience = bs.find(class_="d at").text.split("|")[1]
        try:
            #学历
            education = bs.find(class_="d at").text.split("|")[2]
        except:
            education = "无介绍"

        #请求详情页
        if "https://jobs.51job.com/" in url:
            time.sleep(0.5)
            driver.get(url)
            page_source = driver.page_source
            bs_page = BeautifulSoup(page_source, "lxml")
            text = bs_page.find(class_="bmsg job_msg inbox").text.replace("微信分享","").strip()
            try:
                address = bs_page.find(class_="bmsg inbox").find(class_="fp").text.replace("上班地址：","")
            except:
                address = "无说明"
            print(title)
            cur.execute(sql, (title, company, price, education, experience, welfare,address,text))
            conn.commit()

    if num <= 1:
        next_url = "https://search.51job.com/list/000000,000000,0000,00,9,99,"+str(name)+",2,"+str(num)+".html"
        time.sleep(0.5)
        driver.get(next_url)
        num += 1
        download(driver,driver.page_source,conn,cur)

    return conn,cur

def init_mysql():
    dbparams = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'wad07244058664',
        'database': '51job',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**dbparams)
    cur = conn.cursor()
    return conn,cur

def close_mysql(conn,cur):
    cur.close()
    conn.close()

if __name__ == "__main__":
    name = input("请输入爬取职位名称:")
    text1 = parse.quote(name)
    name = parse.quote(text1)
    driver,source = init()
    conn,cur = init_mysql()
    conn,cur = download(driver,source,conn,cur)
    close_mysql(conn,cur)