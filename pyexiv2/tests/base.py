"""
This script provides the test environment for test cases.
"""
import hashlib
import os
import shutil
from functools import wraps

import psutil
import pytest

from .. import Image, ImageData, set_log_level
from . import reference
from .utils import *


TEST_DIR      = os.path.dirname(__file__)
original_img  = os.path.join(TEST_DIR, '1.jpg')
test_img      = os.path.join(TEST_DIR, 'test.jpg')


def setup_function():
    shutil.copy(original_img, test_img) # Before each test, make a temporary copy of the image


def teardown_function():
    os.remove(test_img)


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
        diff_file_by_md5(original_img, test_img)
        return ret
    return wrapper


def simulate_updating_metadata(raw_dict: dict, changes: dict) -> dict:
    """ Simulate the process of updating the metadata dict by pyexiv2. """
    result = raw_dict.copy()
    result.update(changes)
    for k, v in list(result.items()):
        if v == '':
            result.pop(k)
    return result
