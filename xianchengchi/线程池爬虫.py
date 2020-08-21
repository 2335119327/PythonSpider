import requests
from bs4 import BeautifulSoup
import time
import re
from multiprocessing.dummy import Pool


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.61"
}

dic = {}
urls = []
url = "https://www.pearvideo.com/"

start = time.time()
response = requests.get(url=url, headers=headers)
data = BeautifulSoup(response.text, "lxml")
div_list = data.find_all(class_="ver-act-block pd040")
for div in div_list:
    div_data = BeautifulSoup(str(div), "lxml")
    a_list = div_data.find(class_="vervideo-blist-bd recommend-btbg clearfix").find_all("a")
    for a in a_list:
        if str(a["href"]).split("_")[0] == "video":
            page_url = "https://www.pearvideo.com/" + a["href"]
        else:
            continue

        page_response = requests.get(url=page_url, headers=headers)
        page_data = BeautifulSoup(page_response.text, "lxml")
        name = page_data.find(class_="video-tt").text.strip().replace("|","") + ".mp4"
        time.sleep(0.5)
        ex = 'srcUrl="(.*?)",vdoUrl'
        video_url = re.findall(ex, page_response.text)[0]
        dic = {
            "name": name,
            "url": video_url
        }
        urls.append(dic)
    print("=" * 100)


def Download_video(dic):
    #对视频发起请求获取二进制数据
    data = requests.get(dic["url"],headers=headers).content
    with open(dic["name"],"wb") as f:
        f.write(data)
        print(dic["name"],"下载完毕！")


pool = Pool(4)
pool.map(Download_video,urls)

pool.close()
pool.join()

end = time.time()
print(end-start)