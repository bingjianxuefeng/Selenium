# encoding: utf-8
"""
@author:Administrator
@file: readconfig.py
@time: 2018/11/06
"""
import os
from configparser import ConfigParser

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir,'Data/config.ini'))

def get_config(section,option):
    cf = ConfigParser()
    cf.read(CONFIG_PATH)
    return cf.get(section, option)





if __name__ == "__main__":
    print get_config('server', 'url')