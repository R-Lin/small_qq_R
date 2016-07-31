import requests
print requests.get('http://www.ip.cn/index.php', params={'ip': '1.1.1.1'}).text
