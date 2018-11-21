# encoding: utf-8
"""
@author:Administrator
@file: base_page.py
@time: 2018/11/06
"""

import time
import allure
import pytest
import urllib
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from Unit.log import Log as L
from Unit.log import *
from Unit.tool import Switch
from Unit.tool import capture_binary
from allure.constants import AttachmentType


class BasePage(object):
    """
     @describe:页面的基类,在web中大概的将每一个或者多个页面进行分类,转换成Page的概念.
     @note:    所有的页面类将会继承这个基类.
     """
    driver = None  # 将driver设置为类变量而不是实例变量,目的是为了方便其他子类继承之后直接使用,保持同一个driver
    def __init__(self, driver):
        self.__class__.driver = driver

    # 获取当前页面的aspx的值
    def get_current_aspx(self):
        value = re.findall(r'testin.cn\/(.*?)\/', self.driver.current_url)
        return value[0] if len(value) > 0 else ''


    # ===========================================================================
    # 元素定位的核心方法,基于业务的需要,我们默认这个搜索将会使用显式等待的模式去重复搜索元素.
    # ===========================================================================
    @allure.step(u'等到页面完成加载')
    def wait_page_load_finish(self, timeout=180):
        timeout_message = 'This page has not load finsh for more than %s seconds.' % str(timeout)
        WebDriverWait(self.driver, timeout).until(lambda x: x.execute_script("return document.readyState") == 'complete', message=timeout_message)

    @allure.step(u'通过url进行页面跳转:{1}')
    def get_url(self, url, timeout=10):
        self.wait_page_load_finish(timeout=timeout)
        self.driver.get(url)
        self.wait_page_load_finish(timeout=timeout)

    @allure.step(u'获取当前的url')
    def get_current_url(self):
        url = ''
        try:
            url = urllib.unquote(self.driver.current_url)
        except Exception as e:
            if not expected_conditions.alert_is_present()(self.driver):
                raise
        return url

    @staticmethod
    def get_attribute_by_element(element, name):
        '''返会元素的属性值'''
        return element.get_attribute(name)


    def get_attribute(self, t_element, name):
        '''
        # 得到当前元素的属性的值
        :param t_element: 当前的元素
        :param name: 属性名
        :return:
        '''
        return self.find_element(t_element).get_attribute(name)

    def is_exists_alert(self):
        '''判断存在alert'''
        return True if expected_conditions.alert_is_present()(self.driver) else False

    @allure.step(u'寻找元素列表:{1}')
    def find_elements(self, loc, timeout=10, ele=None, IsErrorStop=True):
        '''

        :param loc: 元素搜索的描述,字典类型:{'type':'id','value':'xxxxx') 或者是元组（id','xxxxx'）
        :param timeout: 超时时间 默认是10s
        :return: 返回搜索到元素列表
        '''
        if isinstance(loc, tuple):
            method = loc[0]
            value = loc[1]
        elif isinstance(loc, dict):
            method = loc['type']
            value = loc['value']
        else:
            raise Exception(u'loc类型错误,无法操作')
        elementList = []
        timeout_message = 'This     elementList has not been found for more than ' + str(timeout) + ' seconds.'
        ele_driver = self.driver if ele is None else ele
        if method is '' or value is '':
            L.warning_log(u'元素描述的type和value不能为空')
        try:
            L.info_log(u'正在寻找的元素：%s' % loc.__str__())
            for case in Switch(method):
                if case('id'):
                    elementList = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_elements_by_id(value), message=timeout_message)
                    break
                if case('xpath'):
                    elementList = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_elements_by_xpath(value), message=timeout_message)
                    break
                if case('name'):
                    elementList = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_elements_by_name(value), message=timeout_message)
                    break
                if case('class'):
                    elementList = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_elements_by_class_name(value), message=timeout_message)
                    break
                if case('tag'):
                    elementList = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_elements_by_tag_name(value), message=timeout_message)
                    break
                if case('link_text'):
                    elementList = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_elements_by_link_text(value), message=timeout_message)
                    break
                if case():
                    L.warning_log(u'不存在的%s 方法，请检查' % method)
                    break
        except TimeoutException as e:
            if IsErrorStop:
                L.error_log(u'未找到元素：%s，原因是:%s' % (loc.__str__(), e.msg))
                raise
        return elementList

    @allure.step(u'寻找元素:{1}')
    def find_element(self, loc, timeout=10, ele=None, IsErrorStop=True):
        '''

        :param loc: 元素搜索的描述,字典类型:{'type':'id','value':'xxxxx') 或者是元组（id','xxxxx'）
        :param timeout: 超时时间 默认是10s
        :return: 返回搜索到元素
        '''
        if isinstance(loc, tuple):
            method = loc[0]
            value = loc[1]
        elif isinstance(loc, dict):
            method = loc['type']
            value = loc['value']
        else:
            raise Exception(u'loc类型错误,无法操作')
        element = ''
        timeout_message = 'This element has not been found for more than ' + str(timeout) + ' seconds.'
        ele_driver = self.driver if ele is None else ele
        if method is '' or value is '':
            L.warning_log(u'元素描述的type和value不能为空')
        try:
            L.info_log(u'正在寻找的元素：%s' % loc.__str__())
            for case in Switch(method):
                if case('id'):
                    element = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_element_by_id(value),
                                                                       message=timeout_message)
                    break
                if case('xpath'):
                    element = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_element_by_xpath(value),
                                                                       message=timeout_message)
                    break
                if case('name'):
                    element = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_element_by_name(value),
                                                                       message=timeout_message)
                    break
                if case('class'):
                    element = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_element_by_class_name(value),
                                                                       message=timeout_message)
                    break
                if case('tag'):
                    element = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_element_by_tag_name(value),
                                                                       message=timeout_message)
                    break
                if case('link_text'):
                    element = WebDriverWait(ele_driver, timeout).until(lambda x: x.find_element_by_link_text(value),
                                                                       message=timeout_message)
                    break
                if case():
                    L.warning_log(u'不存在的%s 方法，请检查' % method)
                    break
        except TimeoutException as e:
            if IsErrorStop:
                L.error_log(u'未找到元素：%s，原因是:%s' % (loc.__str__(), e.msg))
                raise
        return element

    @allure.step(u'点击元素:{0}')
    def click(self, loc, ele=None):
        '''

        :param loc: 元素搜索的描述,字典类型:{'type':'id','value':'xxxxx') 或者是元组（id','xxxxx'）
        :param ele: 点击的元素对象
        :return:
        '''
        element = self.find_element(loc) if ele is None else ele
        self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();', element)
        element.click()
        time.sleep(2)
        L.info_log(u"点击元素：%s" % element.__str__())

    @allure.step(u'点击元素并等待页面响应完成{1}')
    def click_refresh(self, t_element, timeout=180, ele=None, IsClickAlert=True):
        element = self.find_element(t_element) if ele is None else ele
        self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
        element.click()
        time.sleep(1)
        if IsClickAlert:
            self.alert_click()
            self.wait_page_load_finish(timeout=timeout)
            # self.Check_SystemError()
        L.info_log(u'点击元素%s并等待页面响应完成' % str(t_element))

    @allure.step(u'点击元素并等待页面响应完成{1}')
    def click_wait(self, t_element, timeout=180, ele=None):
        element = self.find_element(t_element) if ele is None else ele
        url = self.get_current_url()
        ActionChains(self.driver).move_to_element(element)
        element.click()
        time.sleep(1)
        end_time = time.time() + timeout
        while True:
            new_url = self.get_current_url()
            if new_url != url or new_url != '':
                break
            if time.time() > end_time:
               raise My_LoadFailError(u'点击完元素%s之后超过%s秒浏览器没有任何加载响应' % (t_element, str(timeout)))
            self.wait_page_load_finish()
        L.info_log(u'点击元素%s并等待页面响应完成' % str(t_element))

    @allure.step(u'清空输入框{1}')
    def clear(self, t_element, ele=None,ISEnter=True):
        element = self.find_element(t_element) if ele is None else ele
        element.clear()
        if ISEnter:
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        time.sleep(0.5)
        L.info_log(u'清空输入框:%s' % str(t_element))

    @allure.step(u'输入内容:{1}')
    def send_key(self, t_element, value, ele=None, ISEnter=False, ISAuto=False, ISClear=False, IsAjaxErrorStop=True):
        element = self.find_element(t_element) if ele is None else ele
        if ISClear:
            if self.get_attribute_by_element(element, 'type') != 'file':
                self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
                element.click()
            if self.get_platform_name() == 'Mac':
                self.driver.execute_script("arguments[0].select();", element)
            else:
                element.send_keys(Keys.CONTROL + "a")
                time.sleep(1)
        element.send_keys(str(value))
        L.info_log(u'输入字符串:%s' % str(value))
        time.sleep(1)
        if (element.get_attribute('class') == 'AutoCompleteInput Autocomplete') or (element.get_attribute('class') == 'AutoCompleteInput'):
            if ISAuto:
                InputID = self.get_attribute_by_element(element, 'id')
                locStr = InputID.replace('Input', '') + 'RefListItem0'
                loc = {'type': 'xpath',
                       'value': '//ancestor::section//div//div[@id="%s"]' % locStr}
                self.wait_element_display(loc, timeout=10)
                element2 = self.find_element(loc, IsErrorStop=IsAjaxErrorStop)
                element_div = element2 if element2 else element
                element_div.click()
                element.click()
        if ISEnter:
            ActionChains(self.driver).send_keys(Keys.ENTER).perform()
            time.sleep(2)

    @allure.step(u'下拉框选择{2}')
    def select(self, t_element, value, ByOption=False, ele=None):
        element = self.find_element(t_element) if ele is None else ele
        if ByOption:
            Select(element).select_by_value(value)
        else:
            Select(element).select_by_visible_text(value)
        L.info_log(u'下拉框选择%s' % value)

    @allure.step(u'下拉框带滚动条的选择{2}')
    def select2(self, t_element, value, ele=None):
        SelectEle = self.find_element(t_element) if ele is None else ele
        Select(SelectEle).deselect_all()
        if isinstance(value, str):
            value = (value,)
        for item in value:
            if str(item) != '':
                option = self.find_element(('xpath', '//option[text()="' + str(item) + '"]'), ele=SelectEle)
                ActionChains(self.driver).move_to_element(option).perform()
                self.select(t_element, str(item), ele=SelectEle)
                L.info_log(u'下拉框选择%s' % item)
            ActionChains(self.driver).key_down(Keys.CONTROL)
        ActionChains(self.driver).key_up(Keys.CONTROL)

    @allure.step(u'复选框选择{1}')
    def checkbox(self, t_element, value, ele=None):
        """
        :param t_element:
        :param ele:
        :param value:  Bool type
        :return:
        """
        element = self.find_element(t_element) if ele is None else ele
        self.driver.execute_script("arguments[0].scrollIntoViewIfNeeded();", element)
        ActionChains(self.driver).move_to_element(element).perform()
        if element.is_selected() != value:
            self.click(t_element, ele=element)

    # 等待元素出现或者消失.
    def wait_element(self, loc, ToExists=True, timeout=30, IsErrorStop=True):
        """
        :param IsErrorStop: 目的是为了匹配断言而用,如果ErrorStop为False,则只返回Bool而不抛错
        :param loc:  元素描述
        :param ToExists:  目的是为了等待元素出现还是等待元素消失.默认是等待元素出现
        :param timeout:   等待超时时间,int类型
        :return:  Bool
        """
        if isinstance(loc, tuple):
            method = loc[0]
            value = loc[1]
        elif isinstance(loc, dict):
            method = loc['type']
            value = loc['value']
        if ToExists:
            try:
                element = WebDriverWait(self.driver, timeout).until(lambda x: x.find_element(method, value), timeout)
            except TimeoutException as e:
                if IsErrorStop:
                    raise My_LoadFailError(u'元素%s经过%s秒等待,仍然未出现' % (loc.__str__(), timeout))
                else:
                    return False
        else:
            end_time = time.time() + timeout
            while True:
                try:
                    element = WebDriverWait(self.driver, timeout).until(lambda x: x.find_element(method, value), 5)
                except TimeoutException as e:
                    return True
                if time.time() > end_time:
                    if IsErrorStop:
                        raise My_LoadFailError(u'元素%s超过%s秒仍然存在,测试无法继续,跳出' % (loc.__str__(), timeout))
                    else:
                        return False

    @allure.step('判断元素是否在当前页面显示')
    def is_element_display(self, loc, timeout=10):
        """
        判断loc元素是否显示在当前页面.
        :param loc:
        :return:
        """
        ele = self.find_element(loc, IsErrorStop=False, timeout=timeout)
        if not ele:
            return False
        style = self.get_element_css(ele)
        ele_size = ele.size
        if int(ele_size['height']) > 0 and int(
                ele_size['width']) > 0 and "display: none" not in style and "visibility: hidden" not in style:
            return True
        else:
            return False

    @allure.step('等待元素显示{1}')
    def wait_element_display(self, loc, timeout=30, IsErrorStop=True):
        self.wait_element(loc, ToExists=True, timeout=timeout, IsErrorStop=IsErrorStop)
        end_time = time.time() + timeout
        while True:
            element = self.find_element(loc, timeout=timeout, IsErrorStop=IsErrorStop)
            if not element:
                time.sleep(2)
                continue
            try:
                style = self.get_element_css(element)
                ele_size = element.size
            except StaleElementReferenceException as E:
                time.sleep(2)
                element = self.find_element(loc, timeout=timeout, IsErrorStop=IsErrorStop)
                style = self.get_element_css(element)
                ele_size = element.size
            if int(ele_size['height']) > 0 and int(
                    ele_size['width']) > 0 and "display: none" not in style and "visibility: hidden" not in style:
                return True
            else:
                if time.time() > end_time:
                    if IsErrorStop:
                        raise My_LoadFailError(u'元素%s超过%s秒仍然未显示在用户当前界面,测试无法继续,跳出' % (loc.__str__(), timeout))
                    else:
                        return False
                time.sleep(2)

    @allure.step('等待,直到元素消失:{1}')
    def wait_element_disappear(self, t_element, timeout=30, IsErrorStop=True):
        end_time = time.time() + timeout
        while self.is_element_display(t_element, timeout=2):
            if time.time() > end_time:
                if IsErrorStop:
                    raise My_LoadFailError('元素%s超过%s秒仍然存在,没有消失,测试无法继续,报错跳出' % (t_element.__str__(), str(timeout)))
                else:
                    return False
            time.sleep(1)
        return True

    @allure.step(u"判断alert是否存在,存在就点击确定,否则忽略.")
    def alert_click(self):
        text = ''
        if expected_conditions.alert_is_present()(self.driver):
            self.make_screenshot(u'alert截图', IsWindowsPic=True)
            with pytest.allure.step(u'存在alert,点击确定按钮'):
                text = self.driver.switch_to.alert.text
                self.driver.switch_to.alert.accept()
                # expected_conditions.alert_is_present()(self.driver).accept() ##若存在点击alert上的【确认按钮】
                time.sleep(1)
                self.wait_page_load_finish()
            L.info_log(u'存在alert,点击确定按钮')
        return text

    @allure.step(u'截屏')
    def make_screenshot(self, PicName, IsWindowsPic=True):
        try:
            pytest.alluer.attch(PicName, capture_binary(self.driver, IsWindowsPic=IsWindowsPic), AttachmentType.PNG)
        except Exception as e:
            with pytest.allure.step(u'存在alert,但是截图过程失败'):
                L.error_log(u'存在alert,但是截图过程失败,详细信息:%s' % e.message)

    def get_platform_name(self):
        '''获取设备的名字'''
        return 'Windows' if os.name == 'nt' else 'MAC'


    def get_element_css(self, element):
        js = '''
                function getCurrentStyle(node) {
                    var style = null;
                    if(window.getComputedStyle) {
                        style = window.getComputedStyle(node, null);
                    }else{
                        style = node.currentStyle;
                    }
                    return style;
                }
                style=getCurrentStyle(arguments[0]);
                a=null;  
                return style["cssText"];
            '''
        return self.driver.execute_script(js, element)



def creatsession():
    # 设置Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  #窗口最大化
    options.add_argument("--disable-infobars") #禁用浏览器正在被自动化程序控制的提示)

    #禁止浏览器出现弹框
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs',prefs)
    driver = webdriver.Chrome(chrome_options=options)
    basepage = BasePage(driver)
    return basepage




if __name__ == '__main__':
    creatsession()


