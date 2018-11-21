# encoding: utf-8
"""
@author:Administrator
@file: page_realmachine.py
@time: 2018/11/14
"""
from Base.base_page import BasePage
from Unit.tool import parse
import allure


class Page_RealmaChine(BasePage):
    '''远程真机'''

    def __init__(self, AutoRead=False):
        self.page = {}
        if AutoRead:
            self.read_page()


    def read_page(self):
        self.page = parse(self.get_current_aspx())

    @allure.step(u'进入远程真机:{0}')
    def into_realmachine(self, url):
        self.get_url(url)

    @allure.step(u'点击专有云')
    def click_Proprietarycloud(self):
        self.click_wait(self.page['B_Proprietarycloud'])

    def click_lookrecord(self):
        self.click_wait(self.page['B_lookrecord'])


