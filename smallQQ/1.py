#coding:utf8
import requests
import re
import time
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Host':'w.qq.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
}
s = requests.session()
s.headers.update(header)
login_url = 'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'
html = s.get(login_url, verify=True)
appid = re.findall(r'<input type="hidden" name="aid" value="(\d+)" />', html.text)[0]
sign = re.findall(r'g_login_sig=encodeURIComponent\("(.*?)"\)', html.text)[0]
js_ver = re.findall(r'g_pt_version=encodeURIComponent\("(\d+)"\)', html.text)[0]
mibao_css = re.findall(r'g_mibao_css=encodeURIComponent\("(.+?)"\)', html.text)[0]
start_time = time.mktime(time.gmtime())* 1000
# for k, v in html.cookies.iteritems():
#     s.cookies[k] = v
with open('qrcode.png', 'wb') as f :
    f.write(s.get('https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=L&s=8&d=72&v=4'.format(appid)).content)
url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid={0}&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-{1}&mibao_css={2}&t=undefined&g=1&js_type=0&js_ver={3}&login_sig={4}&pt_randsalt=0'.format(appid,0, mibao_css, js_ver, sign)
print url
# s.headers['Referer'] = login_url
while 1 :
    c = s.get(url)
    print c.text
    time.sleep(2)

