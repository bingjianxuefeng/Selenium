# encoding: utf-8
"""
@author:Administrator
@file: log.py
@time: 2018/11/07
"""
import os
import logging
import time


RUNLOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'Runlog/CaseLog'))



class Log:

    @staticmethod
    def info_log(msg):
        L = Logger()
        L.log.info(msg)

    @staticmethod
    def debug_log(msg):
        L = Logger()
        L.log.info(msg)

    @staticmethod
    def warning_log(msg):
        L = Logger()
        L.log.info(msg)

    @staticmethod
    def error_log(msg):
        L = Logger()
        L.log.info(msg)


class Logger(object):

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.format = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")

        # 这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志 避免重复写日志问题
        if not self.log.handlers:
            file_name = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + '.log'
            file = os.path.abspath(os.path.join(RUNLOG_PATH, file_name))
            self.logfile = logging.FileHandler(file)
            self.logfile.setLevel(logging.INFO)
            self.logfile.setFormatter(self.format)

            self.control = logging.StreamHandler()
            self.control.setLevel(logging.INFO)
            self.control.setFormatter(self.format)

            # if len(self.log.handlers) < 2:
            self.log.addHandler(self.logfile)
            self.log.addHandler(self.control)


class My_SystemError(Exception):
    def __init__(self, arg):
        self.args_ = arg + u',具体页面请看下面附加的:SystemError截图'
        Log.error_log(self.args_)

class My_Http404Error(Exception):
    def __init__(self, arg):
        self.args_ = arg + u',具体页面请看下面附加的:Http404截图'
        Log.error_log(self.args_)

class My_LoadFailError(Exception):
    def __init__(self, arg):
        self.args_ = arg + u',具体页面请看下面附加的:元素加载失败截图'
        Log.error_log(self.args_)

class My_FileDownLoadError(Exception):
    def __init__(self, arg):
        self.args_ = arg + u',具体页面请看下面附加的:文件下载失败截图'
        Log.error_log(self.args_)


if __name__ == '__main__':
    L = Log()
    L.info_log('hi')
    L.info_log('hi too')
    L.info_log('hi three')