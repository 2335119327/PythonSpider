import requests
import os

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
}

data = {
    "params": "S+bTgfrCYNVeGY8R8Oyd4LE1h7q1oSmnxeh/j+XJQ5/1zdbzFlmcye13sJN/n1v7KCeXr9be5zJ8oIFw6uXR1JjjWVbJmgD/TybP9hjM76otLR/oZjHhkyJqoWJ03spw6C5S2u3z+GnRPriYBhz9WxKIcR1BAbFRzjtL2HXz3LH91INcXMlV5KlFw5U3sChQZXpMcbFQmT/mHcjhIszde0jZ0U9ElwUM1Y/ytOjawow6QWkFl91LuOghxBeYf0rPM4cP6dQqp/epvcnI/XX/kw==",
    "encSecKey": "761c3091efc9ed79b07cd8a6fdeb096e70590659cf1f3f87c069dfb912f5c80b62155b3db60687dc5ee402faa48364038dcf672c3b21581ee4d4f17809970d96c208af23e8ec455e73ad7c224c7bdd3f1de38d9120a5d40d58c94fdd2c92439748491ec361dc0915fcb3ee8bcdb287d401f31793455ad1cec75baf9bd8f7641b"
}

response = requests.post(url="https://music.163.com/weapi/cloudsearch/get/web?csrf_token=", headers=headers,data=data).json()

path = "./音乐"
if not os.path.exists(path):  # 做个判断,是否存在此路径,若不存在则创建,注意这个创建的是文件夹，文件夹，文件夹，说三遍
    os.makedirs(path)
for data in response["result"]["songs"]:
    name = data["name"]
    id = data["id"]
    url = "https://api.imjad.cn/cloudmusic/?type=song&id=" + str(id)
    print(url)
    response_data = requests.get(url=url)
    music_url = response_data.json()["data"][0]["url"]
    try:
        res = requests.get(url=music_url,headers=headers).content
    except:
        continue
    # print(music_url)
    with open(path + "/" + name + ".mp3", 'wb')as f:  # 以wb方式打开文件,b就是binary的缩写,代表二进制
        f.write(res)