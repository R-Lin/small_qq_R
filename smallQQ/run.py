# coding:utf8
import re
import sys
import random
import time
import json
import os
import cPickle
import requests
import initialize
import learning


class SmartQQ:
    """
    A simple robot! For Fun!
    """
    def __init__(self):
        self.qtwebqq = None
        self.learn = learning.Learn()
        self.cookie_file = "cookies.txt"
        self.clientid = 53999199
        self.psessionid = ''
        self.vfwebqq = None
        self.friends_list = {}
        self.para_dic = {}
        self.url_request = initialize.get_req()
        self.log = initialize.log()
        self.groupName = {}
        self.groupMember = {}
        self.url_dic = {
            'test': 'https://httpbin.org/post',
            'qrcode': 'https://ssl.ptlogin2.qq.com/ptqrshow?appid={0}&e=0&l=L&s=8&d=72&v=4',
            'get_online_buddies2': 'http://d1.web2.qq.com/channel/get_online_buddies2?vfwebqq={0}4&clientid={1}&psessionid={2}',
            'groupNameList': 'http://s.web2.qq.com/api/get_group_name_list_mask2',
            'groupInfo': 'http://s.web2.qq.com/api/get_group_info_ext2?gcode={0}&vfwebqq={1}&t={2}',
            'pollMessage': 'http://d1.web2.qq.com/channel/poll2',
            'send_qun': 'http://d1.web2.qq.com/channel/send_qun_msg2',
            'get_friends': 'http://s.web2.qq.com/api/get_user_friends2',
            'send_message': 'http://d1.web2.qq.com/channel/send_buddy_msg2',
            'para': (
                'https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&mibao_css=m_webqq'
                '&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&'
                'f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'),
            'check_scan': (
                'https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1&login2qq=1&aid={0[appid]}'
                '&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&ptredirect=0&ptlang='
                '2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-0&mibao_css={0[mibao_css]}'
                '&t=undefined&g=1&js_type=0&js_ver={0[js_ver]}&login_sig={0[sign]}&pt_randsalt=0')
        }

    def qrcode_login(self):
        """
        Downing the QRcode, and scan it to login
        """
        url = self.url_dic['qrcode'].format(self.para_dic['appid'])
        with open('qrcode.png', 'wb') as f:
            f.write(self.url_request.get(url, verify=True).content)
            self.log.info('Qrcode file is qrcode.png ! Please scan qrcode immediatety')
        url = self.url_dic['check_scan'].format(self.para_dic)
        while 1:
            result = eval(self.url_request.get(url, verify=True).text[6:-3])
            self.log.info(result[4])  # return login result
            if result[0] == '0':
                redirect_url = result[2]
                self.url_request.get(redirect_url)  # visit redirect_url to modify the session cookies
                break
            time.sleep(4)

        # Save the cookies
        with open(self.cookie_file, 'w') as filename:
            cPickle.dump(
                requests.utils.dict_from_cookiejar(self.url_request.cookies),
                filename
            )
            self.log.info("Cookies had saved")

    def get_comm_para(self):
        """
        Return a dict that contains appid, sign, js_ver, mibao_cass
        """
        html = self.url_request.get(self.url_dic['para'])
        self.para_dic['appid'] = re.findall(r'<input type="hidden" name="aid" value="(\d+)" />', html.text)[0]
        self.para_dic['sign'] = re.findall(r'g_login_sig=encodeURIComponent\("(.*?)"\)', html.text)[0]
        self.para_dic['js_ver'] = re.findall(r'g_pt_version=encodeURIComponent\("(\d+)"\)', html.text)[0]
        self.para_dic['mibao_css'] = re.findall(r'g_mibao_css=encodeURIComponent\("(.+?)"\)', html.text)[0]

    def login(self):
        if os.path.exists(self.cookie_file):
            cookies_file_mtime = os.stat(self.cookie_file).st_mtime
            during_time = time.time() - cookies_file_mtime
            if during_time <= 7200:
                with open(self.cookie_file) as f:
                    cookies = requests.utils.cookiejar_from_dict(
                        cPickle.load(f)
                    )
                    self.url_request.cookies.update(cookies)
                    self.log.info("Cookies had loaded")
            else:
                self.log.warn('Cookies_file time out')
                self.qrcode_login()
        else:
            self.log.info("Cookies file not found! Please scan the QRcode")
            self.qrcode_login()
        self.qtwebqq = self.url_request.cookies['ptwebqq']

        r_data = {
            'r': '{{"ptwebqq":"{0}","clientid":{1},"psessionid":"{2}","status":"online"}}'.format(
                        self.qtwebqq,
                        self.clientid,
                        self.psessionid,
                    )}
        self.url_request.headers['Referer'] = 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'
        result = json.loads(
            self.url_request.post('http://d1.web2.qq.com/channel/login2', data=r_data).text
        ).get('result', None)
        if result:
            self.psessionid = result['psessionid']
        else:
            self.log.error('Cookies is failed, Please retry by sacning QRCode')
            os.remove(self.cookie_file)
            self.log.error('Cookies is deleted and exit now!')
            sys.exit(3)

        vfwebqq_url = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid={1}&psessionid={2}&t={3}".format(
                        self.qtwebqq,
                        self.clientid,
                        self.psessionid,
                        str(int(time.time()*1000))
                    )
        result2 = json.loads(self.url_request.get(vfwebqq_url).text)
        self.vfwebqq = result2['result']['vfwebqq']
        activate_url = self.url_dic['get_online_buddies2'].format(self.vfwebqq, self.clientid, self.psessionid)
        activate = json.loads(
            self.url_request.get(activate_url).text
            )
        if not activate['retcode']:
            self.log.info('Activate suessfully!')
            self.log.info('Initilizing now! Please wait!')
            self.get_friends_list()
        else:
            self.log.error(
                'Activate failed! Retcode: %s' % activate['retcode']
            )

    def get_hash(self, uin, ptwebqq):
        """
        提取自http://pub.idqqimg.com/smartqq/js/mq.js
        """
        N = [0, 0, 0, 0]
        for t in range(len(ptwebqq)):
            N[t % 4] ^= ord(ptwebqq[t])
        U = ["EC", "OK"]
        V = [0, 0, 0, 0]
        V[0] = int(uin) >> 24 & 255 ^ ord(U[0][0])
        V[1] = int(uin) >> 16 & 255 ^ ord(U[0][1])
        V[2] = int(uin) >> 8 & 255 ^ ord(U[1][0])
        V[3] = int(uin) & 255 ^ ord(U[1][1])
        U = [0, 0, 0, 0, 0, 0, 0, 0]
        for T in range(8):
            if T % 2 == 0:
                U[T] = N[T >> 1]
            else:
                U[T] = V[T >> 1]
        N = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        V = ""
        for T in range(len(U)):
            V += N[U[T] >> 4 & 15]
            V += N[U[T] & 15]
        return V


    def get_friends_list(self ):
        """
        Return the friends_list
        """
        self.log.info("Query the friends list")
        response = self.url_request.post(
            'http://s.web2.qq.com/api/get_user_friends2',
            {
                'r': json.dumps(
                    {
                        "vfwebqq": self.vfwebqq,
                        "hash": self.get_hash('0659030105', self.qtwebqq),
                    }
                )
            },
        )
        result = json.loads(response.text)
        if result.get('retcode', None) == 0:
            for item in result['result']['marknames']:
                self.friends_list[str(item['uin'])] = item['markname']


    def poll(self):
        """
        Poll the messages
        """
        if not self.vfwebqq or not self.psessionid:
            self.log.info("Please login")
            self.login()
        else:
            data = {'r':json.dumps({
                "ptwebqq": self.qtwebqq,
                 "clientid": self.clientid,
                 'psessionid': self.psessionid,
                 "key": ""
                 }
            )}
            while 1:
                try:
                    reponse = self.url_request.post(self.url_dic['pollMessage'], data=data).content
                    mess = json.loads(reponse)
                    for messages in mess['result']:
                        from_uin = str(messages['value']['from_uin'])
                        words = ''.join(messages['value']['content'][1:])
                        if messages['poll_type'] == 'message':
                            self.log.info("The 217 line %s : %s" % (
                                self.friends_list.get(from_uin, 'None'),
                                words
                            ))
                            result = self.learn.learn_or_call(words.replace("\n", r"\\n"))
                            if result:
                                print 224, self.send_single(from_uin, result.replace("\n", r"\\n"))
                                print result
                            else:
                                print 225, result
                                print self.friends_list.get(from_uin, 'None'), " : ", words

                        elif messages['poll_type'] == 'group_message':
                            if from_uin not in self.groupMember:
                                self.log.info('GroupId : %s is not in dict GroupName' % from_uin)
                                self.get_group_info(from_uin)
                            send_uid = str(messages['value']['send_uin'])
                            group_name = self.groupName[from_uin]['name']
                            if isinstance(words, list):
                                print 172, words
                            else:
                                # words = words.encode('utf8', 'ignore')
                                if '/awk/' in group_name:
                                    print '###########################TEST###########################'
                                    result = self.learn.learn_or_call(words.replace("\n", r"\\n"))
                                    if result:
                                        print self.send_messages(from_uin, result)
                                print group_name,
                                print self.groupMember[from_uin][send_uid],  ":" + words.encode('utf8', 'ignore')

                except KeyError as m:
                    if m.message != 'result':
                        self.log.error('KeyError: 131 lines')
                        self.log.error(m)
                        print 133, self.groupName
                        print mess
                    else:
                        self.log.info("Messages time out ! ")

                except TypeError as e:
                    self.log.error(e)
                    self.log.error('TypeError: 176 lines')
                    self.log.error(reponse)

                except ValueError as e:
                    self.log.error(e)
                    print 181, mess
                    self.log.error('ValueError: 140 lines')
                    print 183, self.url_request.post(self.url_dic['pollMessage'], data=data).text

    def send_single(self, to_uin, messages='Test'):
        """
        Send single messages
        """
        data = (
            ('r',
            '{{"to":{0},"content":"[\\"{1}\\",[\\"font\\",{{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","face":693,"clientid":{2},"msg_id":{3},"psessionid":"{4}","service_type":0}}'.format(
             to_uin, messages, self.clientid, random.randint(0, 1000), self.psessionid)),
            ('clientid', self.clientid),
            ('psessionid', self.psessionid)
        )
        result = self.url_request.post(self.url_dic['send_message'], data=data).text
        return result

    def send_messages(self, from_uin, messages='Test_talk'):
        """
        Send group messages
        """
        data = (
            ('r',
             '{{"group_uin":{0}, "face":564,"content":"[\\"{4}\\",[\\"font\\",{{\\"name\\":\\"Arial\\",\\"size\\":\\"10\\",\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}}]]","clientid":{1},"msg_id":{2},"psessionid":"{3}"}}'.format(
                 from_uin, self.clientid, random.randint(0, 1000), self.psessionid, messages)),
            ('clientid', self.clientid),
            ('psessionid', self.psessionid)
        )
        result = self.url_request.post(self.url_dic['send_qun'], data=data).text
        return result

    def get_group_info(self, groupid):
        """
        According the GroupID, to set the GroupName_dic and GroupMem_dic
        """
        self.log.info("Enter function groupInfo")
        response = self.url_request.post(
            'http://s.web2.qq.com/api/get_group_name_list_mask2',
            {
                'r': json.dumps(
                    {
                        "vfwebqq": self.vfwebqq,
                        "hash": self.get_hash('0659030105', self.qtwebqq),
                    }
                )
            },
        )
        result = json.loads(response.text)
        if result['retcode'] == 0:
            for group in result['result']['gnamelist']:
                self.groupName[str(group['gid'])] = group
            self.log.info('Get groupList success!')
            stamp = time.time() * 1000
            group_id = self.groupName[groupid]['code']     # qqqun code
            tmp_dic = {}
            url = self.url_dic['groupInfo'].format(group_id, self.vfwebqq, stamp)
            try:
                member_list = json.loads(self.url_request.get(url).text)['result']['minfo']
                for member in member_list:
                    tmp_dic[str(member['uin'])] = member['nick']
                self.groupMember[str(self.groupName[groupid]['gid'])] = tmp_dic
            except KeyError:
                print "KeyError The line is 187"
                print json.loads(self.url_request.get(url).text)

    def main(self):
        self.get_comm_para()
        self.login()

a = SmartQQ()
a.main()
a.poll()
