# encoding: utf-8
"""
@author:Administrator
@file: runall2.py
@time: 2018/11/24
"""

import pytest

if __name__ == "__main__":
    xml_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Report'))
    args = ['-s', '-q', '--alluredir', xml_file_path]
    pytest.main(args)