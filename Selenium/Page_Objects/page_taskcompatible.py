# encoding: utf-8
"""
@author:Administrator
@file: page_taskcompatible.py
@time: 2018/11/15
"""

import allure
from Base.base_page import BasePage
from Unit.tool import parse



class Page_Task_Compatible(BasePage):
    '''标准兼容性测试'''

    def __init__(self, AutoRead=False):
        self.page = {}
        if AutoRead:
            self.read_page()

    def read_page(self):
        self.page = parse(self.get_current_aspx())

    @allure.step(u'标准兼容性测试:{0}')
    def into_task_compatible(self, url):
        self.get_url(url)

    @allure.step(u'点击开始测试')
    def click_start_test(self):
        self.click_wait(self.page['B_StartTest'])

    @allure.step(u'点击上传应用')
    def click_uploadapp(self):
        self.click(self.page['B_UPLoadApp'])

    @allure.step(u'取消上传文件')
    def click_close(self):
        self.click(self.page['B_close'])