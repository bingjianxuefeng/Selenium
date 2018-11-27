# encoding: utf-8
"""
@author:Administrator
@file: runall2.py
@time: 2018/11/24
"""

import pytest
import sys

if __name__ == "__main__":
    # 启动测试,通过接收cmd参数启动.被用在客户机上被远程调用的时候使用.
    #sys.argv用来接收shell或者是windows批处理传递的参数

    s_len = sys.argv.__len__()
    s_argv = sys.argv
    s_args = ['-s', '-q']
    args = s_args + s_argv[1:]
    # print(s_len)
    # print(s_argv)
    # print(s_argv[1:])
    # print(args)
    pytest.main(s_args)