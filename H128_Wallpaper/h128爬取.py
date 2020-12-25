import requests
import json
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
}

headerss = {
    "authority": "www.h128.com",
    "method": "POST",
    "path": "/tools/newdown.ashx",
    "scheme": "https",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "Content-Length": "31",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "ASP.NET_SessionId=kjp3ivuncrgvrd3mvikjlewc; UM_distinctid=1745d7ca0b8f6-09a842d807704d-15306257-13c680-1745d7ca0b9722; CNZZDATA1277605252=698430799-1599294009-%7C1599294009; dt_cookie_url_referrer=https%3a%2f%2fwww.h128.com%2fshow-33977.html; dt_cookie_user_name_remember=DTcms=%e6%98%9f%e5%85%89%e8%b7%83%e5%bd%b1; dt_cookie_user_pwd_remember=DTcms=5A52611E4039F42BD38AC59D79A76297; Hm_lvt_51f818212e5bab6f247adcaa68213f43=1599296293,1599296815; Hm_lpvt_51f818212e5bab6f247adcaa68213f43=1599297877",
    "Origin": "https://www.h128.com",
    "pragma": "no-cache",
    "Referer": "https://www.h128.com/show-33978.html",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
datas = {
    "site_id": "1",
    "id": "",
    "channel_id": "4",
}

dat_url = "https://www.h128.com/tools/newdown.ashx"
url = "https://www.h128.com/list/0/0/2/0/0/d/1.html"
root = ".//图片//"

response = requests.get(url=url,headers=headers)
response.encoding = 'UTF-8'

data = BeautifulSoup(response.text,"html.parser")

ul = data.find(class_="wrap").find_all("li")
for li in ul:
    data_li = BeautifulSoup(str(li),"html.parser")
    a_url = data_li.select("a")[0]
    #每张图片对应的编号
    num = str(a_url["href"]).split("-")[1].split(".")[0]
    img = data_li.select("a > img:nth-child(2)")[0]
    #图片名称
    alt = img["alt"]
    #图片url
    img_url = img["src"]

    datas["id"] = num
    #中间性请求
    data_response = requests.post(url=dat_url, headers=headerss, data=datas)

    data_res = data_response.text
    print(data_res)
    data_text = json.loads(data_res)
    name = str(data_text["file_path"]).split("/")[6].split(".")[0]


    img_url = img_url.replace('w_487', 'w_1920').replace('h_274', 'h_1080')

    img_url = img_url.replace(url.split("/")[6].split(".")[0], name)

    r = requests.get(url=img_url,headers=headers).content

    path = root + name #图片的名字更改
    with open(path, 'wb') as f:
        f.write(r.content)
        f.close()
        print("文件已保存成功")
