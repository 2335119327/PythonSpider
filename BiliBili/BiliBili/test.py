import requests

url = "https://api.live.bilibili.com/room/v3/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=sort_type_152&page=1&page_size=30"

num = int(url.split("&")[-2].split("=")[1])
num += 1

# next_url = url.replace(url.split("&")[-2].split("=")[1],str(num))
# print(next_url)

print(url.split("&")[-2].split("=")[1])