import requests
import base64



# client_id 为官网获取的AK， client_secret 为官网获取的SK
def get_access_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
    response = requests.get(host)
    access_token = response.json()["access_token"]
    return access_token


request_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/selfie_anime"
# 二进制方式打开图片文件
f = open('1.jpg', 'rb')
img = base64.b64encode(f.read())

#人物图像戴口罩
# params = {
#     "image":img,
#     "type":"anime_mask",
#     "mask_id":"2"
# }

params = {
    "image":img
}

access_token = get_access_token()
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)

image_data = response.json()
if image_data:
    #保存图片
    f = open("2.jpg", 'wb')
    after_img = image_data['image']
    after_img = base64.b64decode(after_img)
    f.write(after_img)
    f.close()
