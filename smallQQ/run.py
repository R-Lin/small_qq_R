# coding:utf8
import cPickle
import json
import os
import random
import re
import sys
import threading
import time
import requests
import initialize
from extends import learning
from extends import broadcast


class SmartQQ:
    """
    A simple robot! For Fun!
    """
    def __init__(self):
        self.qtwebqq = None
        self.cookie_file = "config/cookies.txt"
        self.clientid = 53999199
        self.psessionid = ''
        self.uin = ''
        self.vfwebqq = None
        self.friends_list = {}
        self.para_dic = {}
        self.url_request = initialize.get_req()
        self.log = initialize.log()
        self.learn = learning.Learn()
        self.bc = broadcast.Broadcast()
        self.groupName = {}
        self.groupMember = {}
        self.url_dic = {
            'test': 'https://httpbin.org/post',
            'self_info': 'http://s.web2.qq.com/api/get_self_info2?t=%s',
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
        Downing the QRcode, and scan it to login and saved the cookies file
        """
        url = self.url_dic['qrcode'].format(self.para_dic['appid'])
        with open('config/qrcode.png', 'wb') as f:
            f.write(self.url_request.get(url, verify=True).content)
            self.log.info('Qrcode file is qrcode.png ! Please scan qrcode immediatety')
        url = self.url_dic['check_scan'].format(self.para_dic)

        while 1:
            result = eval(self.url_request.get(url, verify=True).text[6:-3])
            # Return Qrcode scaned result
            self.log.info(result[4])
            if result[0] == '0':
                redirect_url = result[2]
                # Visit redirect_url to modify the session cookies
                self.url_request.get(redirect_url)
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
        """
        If the cookies file existed and not out of the date , login with cookies file, otherwise calls qrcode_login
        """
        self.get_comm_para()
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
            self.get_group_list()
        else:
            self.log.error(
                'Activate failed! Retcode: %s' % activate['retcode']
            )

    def get_hash(self, uin, ptwebqq):
        """
        提取自http://pub.idqqimg.com/smartqq/js/mq.js
        """
        n = [0, 0, 0, 0]
        for t in range(len(ptwebqq)):
            n[t % 4] ^= ord(ptwebqq[t])
        u = ["EC", "OK"]
        v = [0, 0, 0, 0]
        v[0] = int(uin) >> 24 & 255 ^ ord(u[0][0])
        v[1] = int(uin) >> 16 & 255 ^ ord(u[0][1])
        v[2] = int(uin) >> 8 & 255 ^ ord(u[1][0])
        v[3] = int(uin) & 255 ^ ord(u[1][1])
        u = [0, 0, 0, 0, 0, 0, 0, 0]
        for T in range(8):
            if T % 2 == 0:
                u[T] = n[T >> 1]
            else:
                u[T] = v[T >> 1]
        n = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
        v = ""
        for T in range(len(u)):
            v += n[u[T] >> 4 & 15]
            v += n[u[T] & 15]
        return v

    def get_friends_list(self):
        """
        Return the friends_list
        """
        self_info = json.loads(self.url_request.get(
            self.url_dic['self_info'] % (time.time() * 1000)
        ).text)
        self.uin = self_info['result']['uin']
        response = self.url_request.post(
            'http://s.web2.qq.com/api/get_user_friends2',
            {
                'r': json.dumps(
                    {
                        "vfwebqq": self.vfwebqq,
                        "hash": self.get_hash(self.uin, self.qtwebqq),
                    }
                )
            },
        )
        result = json.loads(response.text)
        if result.get('retcode', None) == 0:
            # Get friends markname
            for item in result['result']['marknames']:
                self.friends_list[str(item['uin'])] = item['markname']
        if self.friends_list:
            self.log.info('Friends list initalized suessfully!')
        else:
            self.log.error('Friends list initalized failed!')

            # Get friends nick name!
            for item in result['result']['info']:
                if str(item['uin']) not in self.friends_list:
                    self.friends_list[str(item['uin'])] = item['nick']

            self.log.info("Query the friends list OK")

    def poll(self):
        """
        Poll the messages
        """
        if not self.vfwebqq or not self.psessionid:
            self.log.info("Please login")
            self.login()
        data = {'r': json.dumps(
            {
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
                    words = ' '.join(
                        [i if isinstance(i, unicode) else str(i) for i in messages['value']['content'][1:]]
                    )
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
                            print self.friends_list.get(from_uin, 'None'), " : ", words

                    elif messages['poll_type'] == 'group_message':
                        if from_uin not in self.groupMember:
                            self.log.info('GroupId : %s is not in dict GroupName' % from_uin)
                            self.get_group_member(from_uin)
                        send_uid = str(messages['value']['send_uin'])
                        group_name = self.groupName[from_uin]['name']
                        send_member_name = self.groupMember[from_uin][send_uid]
                        if from_uin in self.bc.gids_set:
                            self.bc.handle_message(
                                (from_uin, group_name, send_member_name, words),
                                self.send_messages
                            )
                        if isinstance(words, list):
                            print 172, words
                        else:
                            # My test group
                            if '/awk/' in group_name:
                                print '###########################TEST###########################'
                                result = self.learn.learn_or_call(words.replace("\n", r"\\n"))
                                if result:
                                    print self.send_messages(from_uin, result)
                            print group_name,
                            print send_member_name,  ":" + words.encode('utf8', 'ignore')
                    else:
                        print "群组聊天没有定义...."

            except KeyError as m:
                if m.message != 'result':
                    self.log.error('%s not in Grount' % (self.get_group_member(from_uin)))
                    self.log.error(m)

                else:
                    self.log.info("No new messages ! ")

            except TypeError as e:
                self.log.error(e)
                self.log.error('TypeError: 176 lines')
                self.log.error(reponse)

            # except ValueError as e:
            #     self.log.error(e)
            #     print 181, mess
            #     self.log.error('ValueError: 140 lines')
            #     print 183, self.url_request.post(self.url_dic['pollMessage'], data=data).text

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

    def _send_member_out_or_join(self, groupid):
        """
        Cheeck member_list for ever ten minutes and
        send Welcome or Sorry info if someone join or leave
        """
        while 1:
            try:
                check_new = self.get_group_member(str(groupid), check_mem=True)
                time.sleep(300)
                check_old, check_new = check_new, self.get_group_member(str(groupid), check_mem=True)
                leave_mem = set(check_old.keys()) - set(check_new.keys())
                join_mem = set(check_new.keys()) - set(check_old.keys())
                if leave_mem:
                    for mem_code in leave_mem:
                        print self.send_messages(
                            str(groupid),
                            'I am sorry ! Group member @%s   was left!' % check_old[mem_code].encode('utf8')
                        )
                if join_mem:
                    for mem_code in join_mem:
                        print self.send_messages(
                            str(groupid),
                            'Welcome! New member @%s was joined!' % check_new[mem_code].encode('utf8')
                            )
            except:
                self.log.error('Thread Exception aborted !')
                break

    def get_group_member(self, groupid, check_mem=False):
        """
         According the GroupID,to set GroupMem_dic
        """
        tmp_dic = {}
        stamp = time.time() * 1000
        # QQ群代码
        group_code = self.groupName[groupid]['code']
        url = self.url_dic['groupInfo'].format(group_code, self.vfwebqq, stamp)
        try:
            member_list = json.loads(self.url_request.get(url).text)['result']

            # 成员马甲
            member_cards = member_list['cards']
            for member in member_cards:
                tmp_dic[str(member['muin'])] = member['card']

            # 成员真实名称
            member_nicks = member_list['minfo']
            for member in member_nicks:
                member_uin = str(member['uin'])
                if member_uin not in tmp_dic:
                    tmp_dic[member_uin] = member['nick']

            self.groupMember[str(self.groupName[groupid]['gid'])] = tmp_dic
            self.log.info('%s : Get groupMemberInfo success!' % self.groupName[groupid]['name'])
            if check_mem:
                return tmp_dic

        except KeyError as e:
            self.log.error(e)
            self.log.error(
                "%s may has no members " % self.groupName[groupid]['name']
            )

    def get_group_list(self):
        """
         Get the GroupName_dic
        """
        response = self.url_request.post(
            'http://s.web2.qq.com/api/get_group_name_list_mask2',
            {
                'r': json.dumps(
                    {
                        "vfwebqq": self.vfwebqq,
                        "hash": self.get_hash(self.uin, self.qtwebqq),
                    }
                )
            },
        )
        result = json.loads(response.text)
        if result['retcode'] == 0:
            bc_ground_code = []
            for group in result['result']['gnamelist']:
                # 收集广播群id
                if group['name'] in self.bc.get_name():
                    bc_ground_code.append(str(group['gid']))

                self.groupName[str(group['gid'])] = group
                if '/awk/sed' in group['name']:
                    check_thread = threading.Thread(
                        target=self._send_member_out_or_join,
                        args=(group['gid'],)
                    )
                    check_thread.setDaemon(True)
                    check_thread.start()
            self.bc.gids_set = set(bc_ground_code)
            self.log.info('Get groupList success!')
        else:
            self.log.error('Get groupList failed!')


if __name__ == '__main__':
    a = SmartQQ()
    a.poll()
