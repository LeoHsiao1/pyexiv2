# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
from functools import wraps

import pytest

from .. import Image, ImageData, set_log_level

current_dir = os.path.dirname(__file__)
original_path = os.path.join(current_dir, '1.jpg')
path = os.path.join(current_dir, 'tmp.jpg')


def setup_function():
    shutil.copy(original_path, path)


def teardown_function():
    os.remove(path)


def _check_md5(file1, file2):
    """ check whether the two files are the same """
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        h1 = hashlib.md5(f1.read()).digest()
        h2 = hashlib.md5(f2.read()).digest()
        return h1 == h2


def check_md5(func):
    """ A decorator that checks if a file has been changed. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        assert _check_md5(path, original_path), 'The file has been changed after {}().'.format(func.__name__)
        return ret
    return wrapper


def compare_dict(d1, d2):
    """ Compare two dictionaries to see if they are the same. """
    assert len(d1) == len(d2)
    for k in d1.keys():
        assert d1[k] == d2[k], "['{}'] is different.".format(k)


def generate_the_correct_result(raw_dict: dict, changes: dict) -> dict:
    ''' Generate the result that supposed to be after modification by pyexiv2.  '''
    correct_result = raw_dict.copy()
    correct_result.update(changes)
    for k, v in list(correct_result.items()):
        if v == '':
            correct_result.pop(k)
    return correct_result
