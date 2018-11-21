# encoding: utf-8
"""
@author:Administrator
@file: test_02.py
@time: 2018/11/15
"""
from Page_Objects import *
import allure
from Unit.runcase import runcase
from Unit.assertp import assert_that

@allure.feature('taskcompatible')
@allure.story('taskcompatible(Medium)')
@runcase
def test_taskcompatible_02(*args):
    task_compatible = Page_Task_Compatible()
    task_compatible.get_url('https://www.testin.cn/task_compatible/list.htm')
    task_compatible.read_page()
    task_compatible.click_start_test()
    task_compatible.click_uploadapp()
    loc = {'type': 'xpath', 'value': '//*[@id="filePicker"]/div[1]'}
    assert_that(loc, description=u'存在点击选择文件按钮').is_exists_element(args[0])
    task_compatible.click_close()


