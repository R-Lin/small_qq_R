#/usr/bin/python
#coding:utf8
import datetime
import time
import requests

def send_messages(phone, messages):
    data = {
      "phone": phone,
      "messageTitle": "[要出发周边游]",
      "content": messages,
      "sendById": 1,
      "userId": 1,
      "userType": 0,
      "objectId": "sample string 6",
      "sendDate": "2016-07-13 17:23:16",
      "scheduleStartTime": "2016-07-13 17:23:16",
      "scheduleEndTime": "2016-07-13 17:23:16",
      "companyId": 1,
      "batchNumber": "sample string 7",
      "fromSystem": "sample string 8",
      "smsContentType": 9,
      "vlinkCommitStatus": 10,
      "vlinkCallStatus": 11
}