# -*- coding: utf-8 -*-
import hashlib
import os
import shutil

import pytest

from .. import Image

current_dir = os.path.dirname(__file__)
jpg_path = os.path.join(current_dir, "1.jpg")
path = os.path.join(current_dir, "tmp.jpg")


def setup_function():
    shutil.copy(jpg_path, path)


def teardown_function():
    # assert check_md5(path, jpg_path), "The file has been changed"
    os.remove(path)


def check_md5(file1, file2):
    """ check whether the two files are the same """
    with open(file1, "rb") as f1:
        h1 = hashlib.md5(f1.read()).digest()
    with open(file2, "rb") as f2:
        h2 = hashlib.md5(f2.read()).digest()
    return h1 == h2


def test_nonexistent_path():
    """ Should report an error. """
    with pytest.raises(RuntimeError):
        Image(os.path.join(current_dir, "0--0.jpg")).read_all()
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_not_image_path():
    """ Should report an error. """
    with pytest.raises(RuntimeError):
        Image(os.path.join(current_dir, "__init__.py")).read_all()
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_chinese_path():
    chinese_path = os.path.join(current_dir, "1 - 副本.jpg")
    shutil.copy(path, chinese_path)
    _dict = {}
    try:
        i = Image(chinese_path)
        _dict = i.read_all()
    finally:
        os.remove(chinese_path)
        assert _dict
        assert check_md5(
            path, jpg_path), "The file has been changed when reading"


def test_read_exif():
    i = Image(path)
    _dict = i.read_exif()
    assert _dict.get("Exif.Image.DateTime", None) == "2019:08:12 19:44:04"
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_read_iptc():
    i = Image(path)
    _dict = i.read_iptc()
    assert _dict.get("Iptc.Application2.TimeCreated", None) == "19:44:04+00:00"
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_read_xmp():
    i = Image(path)
    _dict = i.read_xmp()
    assert _dict.get("Xmp.xmp.CreateDate", None) == "2019-08-12T19:44:04.176"
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_read_all():
    i = Image(path)
    for v in i.read_all().values():
        assert v
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_modify_exif():
    i = Image(path)
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Artist": ""}
    i.modify_exif(dict1)
    _dict = i.read_exif()
    assert _dict.get("Exif.Image.ImageDescription", None) == "test-中文-"
    assert _dict.get("Exif.Image.Artist", None) == None


def test_modify_iptc():
    i = Image(path)
    dict1 = {"Iptc.Application2.ObjectName": "test-中文-",
             "Iptc.Application2.Keywords": ""}
    i.modify_iptc(dict1)
    _dict = i.read_iptc()
    assert _dict.get("Iptc.Application2.ObjectName", None) == "test-中文-"
    assert _dict.get("Iptc.Application2.Keywords", None) == None


def test_modify_xmp():
    i = Image(path)
    dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
             "Xmp.xmp.Rating": ""}
    i.modify_xmp(dict1)
    _dict = i.read_xmp()
    assert _dict.get("Xmp.xmp.CreateDate", None) == "2019-06-23T19:45:17.834"
    assert _dict.get("Xmp.xmp.Rating", None) == None


def test_clear_all():
    i = Image(path)
    i.clear_all()
    for v in i.read_all().values():
        assert not v
