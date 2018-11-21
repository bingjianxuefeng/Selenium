# encoding: utf-8
"""
@author:Administrator
@file: runcase.py
@time: 2018/11/07
"""
import functools
import pytest
import traceback
from Unit.log import Log as L
# Session装饰器,每一个用例都会用到它.
def runcase(func):
    @functools.wraps(func)
    def _runcase(session):
        L.info_log('运行case：%s' % func.__name__)
        try:
            func(session)
        except Exception as e:
            pytest.fail(traceback.format_exc())
    return _runcase












if __name__ == "__main__":
    pass