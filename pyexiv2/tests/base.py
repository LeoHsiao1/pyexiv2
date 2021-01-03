# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
from functools import wraps

import pytest

from .. import Image, ImageData, set_log_level
from . import testdata

current_dir = os.path.dirname(__file__)
original_path = os.path.join(current_dir, '1.jpg')
path = os.path.join(current_dir, 'tmp.jpg')


def setup_function():
    shutil.copy(original_path, path)


def teardown_function():
    os.remove(path)


def diff_file_by_md5(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        v1 = hashlib.md5(f1.read()).digest()
        v2 = hashlib.md5(f2.read()).digest()
        assert v1 == v2, 'The MD5 value of the file has changed.'


def check_md5(func):
    """ A decorator to check if the file has been changed. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        diff_file_by_md5(original_path, path)
        return ret
    return wrapper


def diff_dict(dict1, dict2):
    assert len(dict1) == len(dict2)
    for k in dict1.keys():
        assert dict1[k] == dict2[k], "['{}'] is different.".format(k)


def simulate_updating_metadata(raw_dict: dict, changes: dict) -> dict:
    ''' Simulate the process of updating the metadata dict by pyexiv2.  '''
    result = raw_dict.copy()
    result.update(changes)
    for k, v in list(result.items()):
        if v == '':
            result.pop(k)
    return result
