# encoding: utf-8
"""
@author:Administrator
@file: conftest.py
@time: 2018/11/06
"""
import pytest,time
from Base.base_page import creatsession
from Page_Objects.page_home import logon_testin
from Unit.config import get_config
from Unit.log import Log as L



@pytest.fixture(scope='session')
def session():
    try:
        L.info_log(u'初始化session')
        mybasepage = creatsession()
        logon_testin(get_config('user', 'name'), get_config('user', 'password'))

        yield mybasepage
    except:

        L.warning_log(u'创建session失败')
        raise

    finally:

        mybasepage.driver.quit()






if __name__ == "__main__":
    pass