import requests
from bs4 import BeautifulSoup
import time


proxies_list = []

def download(response):
    global proxies_list
    data_list = BeautifulSoup(response.text, "lxml")
    tr_list = data_list.select("#freelist > table > tbody")
    tr_list = BeautifulSoup(str(tr_list), "lxml")
    for tr in tr_list.find_all("tr"):
        proxies_dict = {}
        td = BeautifulSoup(str(tr), "lxml")
        try:
            http_type = td.find(attrs={"data-title": "类型"}).text.split(",")[1].strip()
        except:
            http_type = td.find(attrs={"data-title": "类型"}).text
        ip = td.find(attrs={"data-title": "IP"}).text
        port = td.find(attrs={"data-title": "PORT"}).text
        # print(http_type, ip, port)
        proxies_dict[http_type] = ip + ":" + port
        proxies_list.append(proxies_dict)




if __name__ == "__main__":
    for i in range(3):
        url = "https://www.kuaidaili.com/ops/proxylist/" + str(i+1)
        response = requests.get(url=url)
        download(response)
    print(proxies_list)
    print("爬虫ip代理个数："+ str(len(proxies_list)))
