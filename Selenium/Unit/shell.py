# encoding: utf-8
"""
@author:Administrator
@file: shell.py
@time: 2018/11/19
"""
import subprocess
#通过shell执行相关的操作

# 注意:像开启个进程不退出的那种cmd命令,不要用这个方法来执行.比如cmd = python

class Shell():
    #args： 要执行的shell命令，可以是字符串，也可以是命令各个参数组成的序列
    # shell设为true，程序将通过shell来执行
    # stdin, stdout, stderr分别表示程序的标准输入、输出、错误句柄。
    # 他们可以是PIPE，文件描述符或文件对象，也可以设置为None，表示从父进程继承。
    # subprocess.PIPE实际上为文本流提供一个缓存区
    @staticmethod
    def run(cmd):
        output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        out = output.decode("gbk").encode("utf-8")
        err = errors.decode("gbk").encode("utf-8")
        return out