import requests
from bs4 import BeautifulSoup
import time
import pymysql


num = 2
sql = "insert into boos(id,title, company, price, education, text, introduce ,address) values(null,%s,%s,%s,%s,%s,%s,%s)"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    "referer": "https://www.zhipin.com/c100010000/?query=python&page=1&ka=page-1",
    "cookie": "_uab_collina=159575841104312945170807; __zp__pub__=; __c=1595890401; lastCity=100010000; JSESSIONID=""; _bl_uid=vLkaCdRI5j77gqrsIh0gbF4mC44z; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1595893052,1595903578,1595903959,1595906815; t=EPTZCBdCrM30pa4h; wt=EPTZCBdCrM30pa4h; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1595913530; __a=50500966.1595758411.1595862833.1595890401.177.4.124.36; __zp_stoken__=67beaGmFLZg0RXnJQY3cBIzMicU9jYzIZF1VdYXwsKBQkPCwGb0tdGEcsOHITTCwFWi49AjoIYy5BJTgsdSFCBVEoc1kTdgEWRSMQRTg3IBNgSQ5DPHsvDSFNcwokCHtOGBd4fT93SAUJYTk%3D"
    # "cookie": "_uab_collina=159575841104312945170807; __zp__pub__=; __c=1595890401; lastCity=100010000; JSESSIONID=""; _bl_uid=vLkaCdRI5j77gqrsIh0gbF4mC44z; sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; __l=l=%2Fwww.zhipin.com%2F&r=https%3A%2F%2Fwww.google.com%2F&friend_source=0&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1595893052,1595903578,1595903959,1595906815; t=EPTZCBdCrM30pa4h; wt=EPTZCBdCrM30pa4h; __a=50500966.1595758411.1595862833.1595890401.190.4.137.49; __zp_stoken__=67beaGmFLZg0RXkh0E2o3IzMicU9fUkEjLl9dYXwsKCx7e0l%2Bb0tdGEcsNmsJbhcFWi49AjoIY3hEUTcsFzsLLTNMa1MZfRAdNykUOTg3IBNgSQ54HmE2AyFNcwokCHtOGBd4fT93SAUJYTk%3D; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1595915805; __zp_sseed__=FpoYYn1oFEBoBycjMy9/wKp0h9sA8EJFanecWnV27w8=; __zp_sname__=77d10f6c; __zp_sts__=1595915816195"
}

proxy = {
    'https': '218.64.148.209:9000'
}

def Crawling(cur,conn,response):
    global num
    global sql

    # 使用lxml XML解析器
    data_list = BeautifulSoup(response.text, "lxml")
    li_list = data_list.find(class_="job-list").find_all("li")


    for data in li_list:
        bs = BeautifulSoup(str(data), "lxml")
        title = bs.find("a")["title"].strip()
        url = "https://www.zhipin.com/" + bs.find("a")['href']
        # 公司
        company = bs.find(class_="company-text").find(class_="name").text
        # 薪资
        price = bs.find(class_="red").text
        # 公司福利
        education = bs.find(class_="info-desc").text
        # print(title+"--"+company+"--"+price+"--"+education)

        # # 请求详情页，进行数据爬取
        # time.sleep(1)
        page_source = requests.get(url=url, headers=headers)
        page_source.encoding = "utf-8"
        page_bs = BeautifulSoup(str(page_source.text), "lxml")
        # 岗位职责
        text = page_bs.find(class_="text").text.strip()
        print(text)
        print("+"*100)
        # 公司介绍
        try:
            introduce = page_bs.find(class_="job-sec company-info").find(class_="text").text.strip()
        except:
            introduce = "无介绍"
        # 工作地址
        address = page_bs.find(class_="location-address").text.replace("502","")

        cur.execute(sql, (title, company, price, education, text, introduce, address))
        conn.commit()

    if num < 4:
        headers["referer"] = "https://www.zhipin.com/c100010000/?query=python&page="+str(num)+"&ka=page-"+str(num)

        next_url = "https://www.zhipin.com/c100010000/?query=python&page="+str(num)+"&ka=page-"+str(num)
        num += 1
        next_data = requests.get(url=next_url,headers=headers,proxies=proxy)
        next_data.encoding = "utf-8"
        Crawling(cur,conn,next_data)
    else:
        return cur,conn




def init_mysql():
    dbparams = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'wad07244058664',
        'database': 'boos',
        'charset': 'utf8'
    }
    conn = pymysql.connect(**dbparams)
    cur = conn.cursor()
    return cur,conn

#关闭数据库连接
def close(cur,conn):
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("="*40)
    requests.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False

    start_url = "https://www.zhipin.com/c100010000/?query=python&page=1&ka=page-1"
    response = requests.get(url=start_url, headers=headers,proxies=proxy)
    time.sleep(2)
    response.encoding = "utf-8"
    # print("="*40)
    print(response.status_code)
    cur,conn = init_mysql()

    cur,conn = Crawling(cur,conn,response)
    close(cur,conn)