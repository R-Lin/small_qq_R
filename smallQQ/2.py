#coding:utf8
import datetime
import time
import requests

data = {
    'r':
        u'{{"group_uin":{0}, "face":564,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"宋体\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","clientid":{1},"msg_id":{2},"psessionid":"{3}"}}'.format(
            1, 1, 1, 1, 1)
}
print requests.post('https://httpbin.org/post', verify=True, data=data).text
