# encoding: utf-8
"""
@author:Administrator
@file: tool.py
@time: 2018/11/07
"""
import yaml
import os
import string
import xlrd
import pandas as pd
from random import Random
from PIL import Image, ImageGrab



def parse(yaml_file):
    '''
    解析指定页面的yaml文件.若不存在,会报出not found file 的异常.
    :param yaml_file: yaml的文件名字,也就是对应页面的名字
    :return: 元素字典.
    '''

    yaml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'Data/yaml', yaml_file + '.yaml'))
    with open(yaml_path, 'r') as f:
        page = yaml.load(f)
    return page['element']


def red_excel_csv(file_name):
    '''
    读取Excel或者是csv
    :param file_name: excel或者是csv的文件
    :return: 字典
    '''
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'Data/TestFile', file_name))
    if '.xlsx' in file_name:
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    return str(df.to_dict(orient='records')).decode('unicode-escape')




# =====================================
# # 实现python不存在的switch-case功能.
#https://www.cnblogs.com/gerrydeng/p/7191927.html
# =====================================

class Switch(object):

    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

def Random_str(randomlength):
    '''
    获取随机字符串
    :param randomlength: 获取随机字符串的长度
    :return:
    '''
    str = ''
    chars = string.ascii_letters + string.digits
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def capture_binary(driver, IsWindowsPic=False):
    '''
    chrome 截屏并返回二进制
    :param driver:
    :param IsWindowsPic:
    :return:
    '''
    tmpimage_name = 'tmp_imag_%s' % Random_str(6)
    if IsWindowsPic:
        image = ImageGrab.grab()
        tmpimage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'Runlog/TmpImage', '%s.png' % tmpimage_name))
        image.save(tmpimage_path)
        with open(tmpimage_path, 'rb') as f:
            binary = f.read()
        os.remove(tmpimage_path)
        return binary
    tmpImage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'Runlog', 'TmpImage'))
    js = 'return window.innerWidth > document.documentElement.clientWidth'
    s = driver.execute_script(js)
    boby_height = driver.execute_script('return document.body.scrollHeight')  # 当前页面的总高度
    pix_h = int(driver.execute_script('return document.documentElement.clientHeight'))  # 当前页面的可见区域高度
    if not s or boby_height < (pix_h * 1.3):
        return driver.get_screenshot_as_png()
    try:
        img_list = []
        i = 0
        while i < 5:
            # 滚屏
            js = "var q=document.body.scrollTop=" + str(i * pix_h) + ";"
            driver.execute_script(js)
            js1 = "return document.body.scrollHeight.toString()+','+document.body.scrollTop.toString()"
            js1_result = driver.execute_script(js1)
            real_scroll_h, real_top = js1_result.split(',')[0], int(js1_result.split(',')[1])
            # real_scroll_h, real_top 是当前滚动条长度和当前滚动条的top，作为是否继续执行的依据，由于存在滚动条向下拉动后会加载新内容的情况，所以需要以下的判断 如果这次设置的top成功，则继续滚屏
            if real_top == (i * pix_h):
                i += 1
                img_path = os.path.abspath(os.path.join(tmpImage_path, tmpimage_name + str(i) + '.png'))
                driver.save_screenshot(img_path)
                img_list.append(img_path)
                last_t = real_top
            else:
                # 如果本次设置失败，看这次的top和上一次记录的top值是否相等，相等则说明没有新加载内容，且已到页面底，跳出循环
                if real_top <= last_t + int(pix_h * 0.3):
                    break
                else:
                    img_path = os.path.abspath(os.path.join(tmpImage_path, tmpimage_name + str(i + 1) + '.png'))
                    driver.save_screenshot(img_path)
                    img_list.append(img_path)
                    break
        output_name = 'tmp_merge_%s.png' % Random_str(10)
        return image_merge(img_list, tmpImage_path, output_name=output_name, binary_data=True)
    except Exception, e:
        print e

def image_merge(images, output_dir, output_name=None, binary_data=False, restriction_max_width=None, restriction_max_height=None):
    """垂直合并多张图片
    images - 要合并的图片路径列表
    ouput_dir - 输出路径
    binary_data - 是否返回二进制数据
    restriction_max_width - 限制合并后的图片最大宽度，如果超过将等比缩小
    restriction_max_height - 限制合并后的图片最大高度，如果超过将等比缩小
    """

    def image_resize(img, size=(1500, 1100)):
        """调整图片大小
        """
        try:
            if img.mode not in ('L', 'RGB'):
                img = img.convert('RGB')
            img = img.resize(size)
        except Exception, e:
            print e
        return img

    max_width = 0
    total_height = 0
    # 计算合成后图片的宽度（以最宽的为准）和高度
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            if width > max_width:
                max_width = width
            total_height += height

            # 产生一张空白图
    new_img = Image.new('RGB', (max_width, total_height), 255)
    # 合并
    x = y = 0
    for img_path in images:
        if os.path.exists(img_path):
            img = Image.open(img_path)
            width, height = img.size
            new_img.paste(img, (x, y))
            y += height

    if restriction_max_width and max_width >= restriction_max_width:
        # 如果宽带超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(max_width)
        max_width = restriction_max_width
        total_height = int(total_height * ratio)
        new_img = image_resize(new_img, size=(max_width, total_height))

    if restriction_max_height and total_height >= restriction_max_height:
        # 如果高度超过限制
        # 等比例缩小
        ratio = restriction_max_height / float(total_height)
        max_width = int(max_width * ratio)
        total_height = restriction_max_height
        new_img = image_resize(new_img, size=(max_width, total_height))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    save_path = '%s/%s' % (output_dir, output_name)
    new_img.save(save_path)
    for img_path in images:
        os.remove(img_path)
    if binary_data:
        with open(save_path, 'rb') as f:
            binary = f.read()
        os.remove(save_path)
        return binary
    return save_path


if __name__ == "__main__":

    test_dic = red_excel_csv('Testin.xlsx')
