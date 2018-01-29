# DEPENDENCY( itchat )


import itchat
import os

from vars import qr_text_dir


class WechatAPI:
    def __init__(self):

        self.hdl = itchat.originInstance

    # noinspection PyMethodMayBeStatic
    def save_qr_text(self, *args, **kwargs):
        with open(qr_text_dir, 'w') as f:
            f.write("https://login.weixin.qq.com/l/" + kwargs['uuid'])

    def login(self):
        self.hdl.login(qrCallback=self.save_qr_text)

    def get_friend(self, target):
        res = self.hdl.get_friends()
        for i in res:
            if i['RemarkName'] == target:
                print(i['UserName'])
                return i['UserName']
        return ''

    def send_file(self, path, to):
        path = os.path.expanduser(path)
        to = self.get_friend(to)
        if to != '':
            print(self.hdl.send('@fil@%s' % path, toUserName=to))

    def send_msg(self, msg, to):
        to = self.get_friend(to)
        if to != '':
            print(self.hdl.send_msg(msg, toUserName=to))

    def reset(self):
        if self.hdl is not None:
            try:
                self.hdl.logout()
            except Exception as e:
                print(e)
            itchat.instanceList.clear()
            self.hdl = itchat.new_instance()
