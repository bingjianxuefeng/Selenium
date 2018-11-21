# encoding: utf-8
"""
@author:Administrator
@file: test_01.py
@time: 2018/11/14
"""

from Page_Objects import *
import allure
from Unit.runcase import runcase
from Unit.assertp import assert_that

@allure.feature('realmachine')
# @allure.story('realmachine(Medium)')
@allure.story('taskcompatible(Medium)')
@runcase
def test_realmachine_01(*args):
    real_machine = Page_RealmaChine()
    url ='https://www.testin.cn/realmachine/index.htm'
    real_machine.into_realmachine(url)
    real_machine.read_page()
    real_machine.click_Proprietarycloud()
    currnet_handle = real_machine.driver.current_window_handle
    real_machine.click_wait(real_machine.page['B_lookrecord'])
    handles = real_machine.driver.window_handles
    for handle in handles:
        if handle != currnet_handle:
            real_machine.driver.switch_to_window(handle)
    loc = {'type': 'xpath', 'value': '//div[@class="table-bordered"]/table//tr[2]//td/a'}
    assert_that(loc).is_exists_element(args[0])
    real_machine.driver.close()
    real_machine.driver.switch_to_window(currnet_handle)































