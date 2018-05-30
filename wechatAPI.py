# DEPENDENCY( selenium )
import time
from queue import Queue
from threading import Thread

import selenium.common.exceptions as SExceptions
from selenium import webdriver
import os

from vars import qr_text_dir

os.environ["webdriver.chrome.driver"] = "chromedriver"


class WechatAPI:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome("chromedriver", chrome_options=self.options)
        self.request_queue = Queue()
        self.online = False

    def __del__(self):
        try:
            self.driver.close()
        except Exception as e:
            pass

    def login(self):
        self.driver.get('https://wx.qq.com/')
        login_cred = self.driver.find_element_by_class_name("qrcode").find_element_by_class_name("img").get_attribute(
            "mm-src").split("/")[-1]
        with open(qr_text_dir, 'w') as f:
            f.write("https://login.weixin.qq.com/l/" + login_cred)
        self.online = True
        t = Thread(target=self.do_task)
        t.daemon = True
        t.start()
        # todo, generate cmd qrcode

    def switch_contact_to(self, contact):
        search_bar = self.driver.find_element_by_class_name("search_bar")
        input_bar = search_bar.find_element_by_css_selector("input")
        input_bar.clear()
        input_bar.click()
        input_bar.send_keys(contact)
        self.driver.implicitly_wait(1)
        candidate_pops = search_bar.find_element_by_class_name("mmpop")
        candidates = candidate_pops.find_elements_by_class_name("ng-scope")
        for c in candidates:
            try:
                if c.find_element_by_class_name("nickname").text == contact:
                    c.find_element_by_class_name("nickname").click()
                    break
            except Exception as e:
                pass

    def append_task(self, task_type, payload, to):
        self.request_queue.put((task_type, payload, to))

    def do_task(self):
        while self.online:
            try:
                (task_type, payload, to) = self.request_queue.get()
                if task_type == "msg":
                    self.send_msg(payload, to)
                    time.sleep(.8)
                elif task_type == "file":
                    self.send_file(payload, to)
                    time.sleep(2)
                self.request_queue.task_done()
            except Exception as e:
                print(e)


    def send_file(self, path, to):
        path = os.path.expanduser(path)
        self.switch_contact_to(to)
        self.driver.find_element_by_xpath('//input[@type="file"]').send_keys(path)

    def send_msg(self, msg, to):
        self.switch_contact_to(to)
        chat_area = self.driver.find_element_by_id("chatArea")
        edit_area = chat_area.find_element_by_id("editArea")
        edit_area.clear()
        edit_area.send_keys(msg)
        self.driver.implicitly_wait(.5)
        chat_area.find_element_by_class_name("btn_send").click()
