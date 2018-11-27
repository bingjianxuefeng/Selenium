# encoding: utf-8
"""
@author:Administrator
@file: Testin_login.py
@time: 2018/10/{DAY}
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import sys
import pytest
from Unit.log import Log as L
from Unit.shell import Shell
def login():
    driver = webdriver.Chrome()
    driver.get('https://www.testin.cn/account/login.htm')
    time.sleep(10)
    driver.maximize_window()
    time.sleep(2)
    element = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('email'))
    element.send_keys('wanghao7025@163.com')
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('pwd')).send_keys('wanghao7025')
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('submitBtn')).click()
    time.sleep(10)
    handle = driver.current_window_handle
    driver.get('https://www.testin.cn/realmachine/index.htm')
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('records_button')).click()
    time.sleep(2)
    handles = driver.window_handles
    time.sleep(2)




if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    report_folder = time.strftime("%Y%m%d%H%M%S")
    xml_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Report', report_folder))
    html_file_path = os.path.abspath(os.path.join(xml_file_path, 'html'))

    # 如果你需要调试单个用例,用feature执行,将feature改为指定的名字即可.
    # args = ['-s', '-q', '--alluredir', xml_file_path, '--allure_stories', 'taskcompatible(Medium)']
    args = ['-s', '-q', '--alluredir', xml_file_path]
    pytest.main(args)

    #利用allure生成html报告
    cmd = 'allure generate %s -o %s' % (xml_file_path, html_file_path)
    print(cmd)

    try:
        Shell.run(cmd)
        L.info_log(u'html报告生成成功')
    except Exception as err:
        L.error_log(u'html报告生成失败,请确保是否安装了allure-commandline,错误信息:%s' %err.args)