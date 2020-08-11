from selenium import webdriver
import time
import pymysql
from bs4 import BeautifulSoup


num = 1

#初始化Selenium
def init():
    name = input("请输入工作:")

    driver = webdriver.Chrome()
    #全屏
    driver.maximize_window()
    driver.get("https://www.lagou.com/")
    driver.find_element_by_id("cboxClose").click()
    time.sleep(1)
    driver.find_element_by_id("search_input").send_keys(str(name))
    time.sleep(0.5)
    driver.find_element_by_id("search_button").click()
    time.sleep(1)
    driver.find_element_by_class_name("body-btn").click()
    source = driver.page_source
    return source,driver

#初始化mysql
def init_mysql():
    dbparams = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'wad07244058664',
        'database': 'lagou',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**dbparams)
    cur = conn.cursor()
    return cur,conn


#数据爬取
def index(cur,source,driver):
    global num

    sql = "insert into lagou(id,title, company, price, experience, education, text, address) values(null,%s,%s,%s,%s,%s,%s,%s)"

    bs = BeautifulSoup(source, "lxml")
    li_list = bs.find_all(class_="con_list_item default_list")
    for li in li_list:
        bs = BeautifulSoup(str(li), "lxml")
        title = bs.find("li")["data-positionname"]
        company = bs.find("li")["data-company"]
        url = bs.find(class_="position_link")["href"]

        #请求详情页，进行数据爬取
        driver.get(url)
        page_source = driver.page_source
        page_bs = BeautifulSoup(page_source, "lxml")
        data = page_bs.find(class_="job_request").text.strip()
        price = data.split("/")[0].strip().split("·")[0]
        experience = data.split("/")[2].strip()
        education = data.split("/")[3].strip()
        text = page_bs.find(class_="job-detail").text.strip()
        address = page_bs.find(class_="work_addr").text.strip().replace(" ", "").replace("查看地图", "").split("-")
        addr = ""
        for addre in address:
            addr += addre + "-"
        addr = addr.rstrip("-")
        cur.execute(sql, (title, company, price, experience, education, text, addr))
        conn.commit()

    for i in range(14):
        driver.back()

    if num <= 3:
        print(num)
        num += 1
        #点击下一页
        time.sleep(5)
        driver.find_element_by_class_name("pager_next").click()
        time.sleep(0.5)
        next_source = driver.page_source
        index(cur,next_source, driver)


#关闭数据库连接
def close(cur,conn):
    cur.close()
    conn.close()

#开始
if __name__ == "__main__":
    source,driver = init()
    cur, conn = init_mysql()
    index(cur,source,driver)
    close(cur,conn)