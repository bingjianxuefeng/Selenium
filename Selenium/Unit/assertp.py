# encoding: utf-8
"""
@author:Administrator
@file: assert.py
@time: 2018/11/13
"""
import allure
from log import Log as L
from Base import base_page



class AssertionBuilder(object):
    """Assertion builder."""

    def __init__(self, val, description='', kind=None):
        """Construct the assertion builder."""
        self.val = val
        self.description = description
        self.kind = kind

    @allure.step(u'断言:验证相等')
    def is_equal_to(self, other):
        """Asserts that val is equal to other."""
        if self.val != other:
            # print(type(self.val))
            # print(type(other))
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (
                self.val.__str__() if type(self.val) in (list, tuple) else self.val,
                other.__str__() if type(other) in (list, tuple) else other))
        else:
            self._normal('Expected <%s> to be equal to Actual <%s>, assert success.' % (
                self.val.__str__() if type(self.val) in (list, tuple) else self.val,
                other.__str__() if type(other) in (list, tuple) else other))
        return self

    @allure.step(u'断言:验证为空')
    def is_null(self):
        """Asserts that val is '' or None"""
        if self.val != '' and self.val is not None:
            self._err('Expected <None> ,but Actual <%s>, assert fail.' % self.val)
        else:
            self._normal('Expected <None> to be equal to Actual <%s>, assert success.' % self.val)
        return self

    @allure.step(u'断言:验证不为空')
    def is_not_null(self):
        A = []
        A.__str__()
        """Asserts that val not is '' or None"""
        if self.val == '':
            self.val = None
        if self.val == '' or self.val is None:
            self._err('Expected <Not None> ,but Actual <%s>, assert fail.'% (self.val.__str__() if type(self.val) in (list, tuple)
                      else self.val))
        else:
            self._normal('Expected <Not None> to be equal to Actual <%s>, assert success.'% (self.val.__str__() if type(self.val) in (list, tuple)
                      else self.val))
        return self

    @allure.step(u'断言:验证元素存在')
    def is_exists_element(self, driver, timeout=10):
        """Asserts that val is not equal to other. self.val must is webelement loc
        :param timeout:
        :param driver:a instance of BasePage
        :return:
        """
        ele = driver.find_element(self.val,timeout=timeout, IsErrorStop=False)
        self.description = 'Element: %s' % self.val.__str__()
        if not ele:
            self._err('Expected <Exists> ,but Actual <Not Exists>, assert fail.')
        else:
            self._normal('Expected <Exists> ,but Actual <Exists>, assert success.')
        return self

    """后面需要哪些类型的断言的时候,请自己添加."""

    @allure.step(u'断言:验证不等于')
    def is_notequal_to(self, other):
        """Asserts that val is not equal to other."""
        if self.val == other:
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (self.val, other))
        else:
            self._normal('Expected <%s> to be not equal to Actual <%s>, assert success.' % (self.val, other))
        return self

    @allure.step(u'断言:验证小于等于')
    def is_smallorequal_to(self, other):
        """Asserts that val is equal to other."""
        if self.val > other:
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (self.val, other))
        else:
            self._normal('Expected <%s> to be small or equal to Actual <%s>, assert success.' % (self.val, other))
        return self

    @allure.step(u'断言:验证大于等于')
    def is_greatorequal_to(self, other):
        """Asserts that val is equal to other."""
        if self.val < other:
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (self.val, other))
        else:
            self._normal('Expected <%s> to be greater or equal to Actual <%s>, assert success.' % (self.val, other))
        return self

    @allure.step(u'断言:验证为True')
    def is_true(self):
        """Asserts that val is equal to other."""
        if not self.val:
            self._err('Expected <True> ,but Actual <%s>, assert fail.' % self.val)
        else:
            self._normal('Expected <True> ,but Actual <%s>, assert success.' % self.val)
        return self

    @allure.step(u'断言:验证字符串在另一个字符串中')
    def is_substring(self, other):
        if self.val not in other:
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (self.val, other))
        else:
            self._normal('Expected <%s> in Actual <%s>, assert success.' % (self.val, other))
        return self

    @allure.step(u'断言:验证字符串存在于某列表中')
    def is_exists_list(self, other):
        """
        :param other:  List type
        :return:
        """
        if self.val not in other:
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (self.val, other))
        else:
            self._normal('Expected <%s> in Actual <%s>, assert success.' % (self.val, other))
        return self

    @allure.step(u'断言:验证字符串不存在于某列表中')
    def is_not_exists_list(self, other):
        '''
        :param other:
        :return:
        '''
        if self.val in other:
            self._err('Expected <%s> ,but Actual <%s>, assert fail.' % (self.val, other))
        else:
            self._normal('Expected <%s> not in Actual <%s>, assert success.' % (self.val, other))
        return self

    @allure.step(u'断言:验证字符串是合法的Json格式')
    def is_json(self):
        import json
        try:
            json.loads(self.val)
            self._normal('Expected <Json> ,but Actual <Json>, assert success.')
        except ValueError:
            self._err('Expected <Json> ,but Actual <Not Json>, assert fail.')
            # L.error_log(self.val)
        return self

    @allure.step(u'断言:对比两个列表')
    def comparelist(self, other):
        if self.val == other:
            self._normal('Expected <%s> ,but Actual <%s>, assert success.' % (self.val, other))
        else:
            self._err('Expected <%s> in Actual <%s>, assert fail.' % (self.val, other))
        return self

    def _err(self, msg):
        """Helper to raise an AssertionError, and optionally prepend custom description."""
        out = '%s%s' % ('[%s] ' % self.description if len(self.description) > 0 else '', msg)
        if self.kind == 'warn':
            L.warning_log(out)
            return self
        else:
            L.error_log(out)
            with allure.step('Assert Fail, Info::%s' % out):
                raise AssertionError(out)

    def _normal(self, msg):
        """Helper to raise an AssertionError, and optionally prepend custom description."""
        out = '%s%s' % ('[%s] ' % self.description if len(self.description) > 0 else '', msg)
        L.info_log(out)
        with allure.step('Assert Success, Info::%s' % out):
            return self

def assert_that(val, description=''):
    L.info_log(u'开始断言验证')
    return AssertionBuilder(val, description=description)

if __name__ == '__main__':
    pass
