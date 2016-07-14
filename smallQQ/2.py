#/usr/bin/python
#coding:utf8
import hashlib
import time
import json
import base64
import requests
from M2Crypto.EVP import Cipher
import pyDes


def sentmessage(message, phone):

    url = 'http://api.yaochufa.com/v2/Sms/SendSMS'
    key = 'abcdefghijklmnopqrstuvwx'


    _json_data = {
      "companyId": "1",
      "content": message,
      "messageTitle": "Zabbix",
      "phone": phone,
      "sendBy": "Zabbix",
      "templateCode": "ZabbixWarn",

    }
    data = json.JSONEncoder().encode(_json_data)
    # 加密
    current_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    mingwen_json = '###'.join([data, current_time, 'abc!@cd'])
    m2 = hashlib.md5()
    m2.update(mingwen_json)
    md5_data = m2.hexdigest()
    jsonandmd5 = '###'.join([data, current_time, md5_data])

    en3ds = encrypt_3des(key, jsonandmd5)
    sent_message = base64.b64encode(en3ds)

    # post请求
    # print sent_message
    s = requests.Session()
    s.headers.update({'content-type': 'application/json'})
    status = s.post(url, sent_message)
    resp_txt = status.text.strip('"')
    # 返回信息解码
    # t_des = pyDes.triple_des(key=key, IV='12345678', mode=pyDes.CBC, padmode=pyDes.PAD_NORMAL)
    tmp = base64.decodestring(resp_txt)
    print data
    print decrypt_3des(key, tmp)

def encrypt_3des(key, text):
    encryptor = Cipher(alg='des_ede3_cbc', key=key, op=1, iv='12345678' * 16)
    s = encryptor.update(text)
    return s + encryptor.final()


def decrypt_3des(key, text):

    decryptor = pyDes.triple_des(key=key, IV='12345678', mode=pyDes.CBC, padmode=pyDes.PAD_NORMAL)
    return decryptor.decrypt(text)

sentmessage("test", '13640882018')
