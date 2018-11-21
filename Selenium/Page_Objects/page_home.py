# encoding: utf-8
"""
@author:Administrator
@file: page_home.py
@time: 2018/11/07
"""
from Base.base_page import BasePage
from Unit.tool import parse
import re
from Unit.config import get_config



class PageHome(BasePage):

    def __init__(self,AutoRead=False):
        self.page = {}
        if AutoRead:
            self.read_page()

    def read_page(self):
        self.page = parse(self.get_current_aspx())



def logon_testin(useremail,password):

    page_home = PageHome()
    log_url = 'https://' + get_config('server', 'url')
    page_home.get_url(log_url)
    page_home.read_page()
    page_home.send_key(page_home.page['account']['O_user'], useremail)
    page_home.send_key(page_home.page['account']['O_password'], password)
    page_home.click_wait(page_home.page['account']['B_logon'])
    page_home.click_wait(page_home.page['enterprise']['O_Company'])


if __name__ == "__main__":
    from Base.base_page import creatsession
    creatsession()
    useremail = get_config('user', 'name')
    password = get_config('user', 'password')
    logon_testin(useremail, password)

