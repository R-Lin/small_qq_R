#/usr/bin/python
#coding:utf8
import datetime
import time
import json
import requests

def send_messages(phone, messages):
    api_url = "http://192.168.9.221:828/v2/Message/SendSmsToWithEncryption"
    data = json.dumps({
        "phone": phone,
        "messageTitle": "[要出发周边游]",
        "content": messages,
        "sendById": 1,
        "userId": 1,
        "userType": 0,
        "objectId": "sample string 6",
        "companyId": 1,
        "batchNumber": "sample string 7",
        "scheduleStartTime": "2016-07-13 17:23:16",
        "scheduleEndTime": "2016-07-13 17:23:16",
        "fromSystem": "sample string 8",
        "smsContentType": 9,
        "vlinkCommitStatus": 10,
        "vlinkCallStatus": 11
    })
    html = requests.post(api_url, data=data)
    print html

send_messages('13640882018', 'hello')
