"""
This script provides the test environment for test cases.
"""
import hashlib
import os
import shutil
from functools import wraps

import psutil
import pytest

from . import reference


class ENV:
    name_for_import_pyexiv2  = os.environ.get('NAME_FOR_IMPORT_PYEXIV2') or '..'
    test_dir      = os.path.dirname(__file__)
    original_img  = os.path.join(test_dir, '1.jpg')
    test_img      = os.path.join(test_dir, 'test.jpg')
    test_img_copy = os.path.join(test_dir, 'test-copy.jpg')
    skip_test     = False


if ENV.name_for_import_pyexiv2 == '..':
    from ..         import Image, ImageData, set_log_level
elif ENV.name_for_import_pyexiv2 == 'pyexiv2':
    from pyexiv2    import Image, ImageData, set_log_level


def setup_function():
    if ENV.skip_test:
        pytest.skip()
    shutil.copy(ENV.original_img, ENV.test_img)  # Before each test, make a temporary copy of the image
    ENV.img = Image(ENV.test_img)


def teardown_function():
    ENV.img.close()
    os.remove(ENV.test_img)


def diff_text(text1: (str, bytes), text2: (str, bytes)):
    max_len = max(len(text1), len(text2))
    for i in range(max_len):
        assert text1[i:i+1] == text2[i:i+1], "The two text is different at index {} :\n{}\n{}".format(i, text1[i:i+10], text2[i:i+10])


def diff_dict(dict1, dict2):
    assert len(dict1) == len(dict2), "The two dict are of different length: {}, {}".format(len(dict1), len(dict2))
    for k in dict1.keys():
        assert dict1[k] == dict2[k], "['{}'] is different.".format(k)


def check_img_md5():
    with open(ENV.original_img, "rb") as f1, open(ENV.test_img, "rb") as f2:
        v1 = hashlib.md5(f1.read()).digest()
        v2 = hashlib.md5(f2.read()).digest()
        assert v1 == v2, 'The MD5 value of the image has changed.'


def simulate_updating_metadata(raw_dict: dict, changes: dict) -> dict:
    """ Simulate the process of updating the metadata dict by pyexiv2. """
    result = raw_dict.copy()
    result.update(changes)
    for k, v in list(result.items()):
        if v == '':
            result.pop(k)
    return result


def check_the_copy_of_img(diff, reference, method_name):
    """ Copy the image and check it, in case the modified data is not saved to disk. """
    try:
        shutil.copy(ENV.test_img, ENV.test_img_copy)
        with Image(ENV.test_img_copy) as img:
            diff(reference, getattr(img, method_name)())
    finally:
        os.remove(ENV.test_img_copy)

