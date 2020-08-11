import requests
from hashlib import md5

class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password = password.encode('utf8')

        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                          headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()


# chaojiying = Chaojiying_Client('ppx666', '07244058664', '906006')  # 用户中心>>软件ID 生成一个替换 96001
# im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
# print(chaojiying.PostPic(im, 9004)['pic_str'])  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

from selenium import webdriver
from PIL import Image
import time
from selenium.webdriver import ActionChains


bro = webdriver.Chrome()
#全屏
bro.maximize_window()

bro.get("https://kyfw.12306.cn/otn/resources/login.html")
time.sleep(2)
bro.find_element_by_class_name("login-hd-account").click()


# save_screenshot 就是将当前页面进行截图且保存
bro.save_screenshot('aa.png')

# 确定验证码图片对应的左上角和右下角的坐标
code_img_ele = bro.find_element_by_id("J-loginImg")
location = code_img_ele.location  #验证码图片左上角的坐标 x,y
size = code_img_ele.size  # 验证码的标签对应的长和宽
# 左上角和右下角的坐标
rangle = (
    int(location['x']),int(location['y']),int(location['x'] + size['width']),int(location['y'] + size['height'])
)

i = Image.open("./aa.png")
code_img_name = './code.png'
# crop裁剪
frame = i.crop(rangle)
frame.save(code_img_name)

chaojiying = Chaojiying_Client('ppx666', '07244058664', '906006')  # 用户中心>>软件ID 生成一个替换 96001
im = open('code.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
print(chaojiying.PostPic(im, 9004)['pic_str'])  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

result = chaojiying.PostPic(im, 9004)['pic_str']
all_list = []  # 存储即将被点击的坐标
if '|' in result:
    list_1 = result.split("|")
    count_1 = len(list_1)
    for i in range(count_1):
        xy_list = []
        x = int(list_1[i].split(",")[0])
        y = int(list_1[i].split(",")[1])
        xy_list.append(x)
        xy_list.append(y)
        all_list.append(xy_list)
else:
    x = int(result.split(",")[0])
    y = int(result.split(",")[1])
    xy_list = []
    xy_list.append(x)
    xy_list.append(y)
    all_list.append(xy_list)
print(all_list)
# 遍历列表，使用动作链对每一个列表元素对应的x,y指定的位置进行点击操作
for l in all_list:
    x = l[0]
    print(x)
    y = l[1]
    print(y)
    ActionChains(bro).move_to_element_with_offset(code_img_ele,x,y).click().perform()   # move_to_element_with_offset   移动到距某个元素（左上角坐标）多少距离的位置
    time.sleep(0.5)

bro.find_element_by_id("J-userName").send_keys("13597971392")
time.sleep(1)
bro.find_element_by_id("J-password").send_keys("wad07244058664")
time.sleep(1)
bro.find_element_by_id("J-login").click()
time.sleep(1)