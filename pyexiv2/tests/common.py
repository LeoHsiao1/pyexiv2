# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
from functools import wraps

import pytest

from .. import Image

current_dir = os.path.dirname(__file__)
jpg_path = os.path.join(current_dir, "1.jpg")
path = os.path.join(current_dir, "tmp.jpg")


def setup_function():
    shutil.copy(jpg_path, path)


def teardown_function():
    os.remove(path)


def _check_md5(file1, file2):
    """ check whether the two files are the same """
    with open(file1, "rb") as f1:
        h1 = hashlib.md5(f1.read()).digest()
    with open(file2, "rb") as f2:
        h2 = hashlib.md5(f2.read()).digest()
    return h1 == h2


def check_md5(func):
    """ A decorator that checks if a file has been changed. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        assert _check_md5(path, jpg_path), "The file has been changed after {}().".format(func.__name__)
        return ret
    return wrapper
