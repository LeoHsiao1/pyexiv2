# -*- coding: utf-8 -*-
import os
import hashlib

import psutil
import pytest

from .. import Image


current_dir = os.path.dirname(__file__)
img_path = os.path.join(current_dir, "tmp.jpg")
jpg_path = os.path.join(current_dir, "1.jpg")


def setup_function():
    if os.path.exists(img_path):
        os.remove(img_path)
    os.link(jpg_path, img_path)


def teardown_function():
    try:
        assert compare(jpg_path, img_path), "The file has been changed"
    finally:
        os.remove(img_path)


def compare(file1, file2):
    """ Determine whether the  two files are identical """
    with open(file1, "rb") as f1:
        with open(file2, "rb") as f2:
            return hashlib.md5(f1.read()).digest() == hashlib.md5(f2.read()).digest()


def test_nonexistent_path():
    """ Should report an error. """
    with pytest.raises(RuntimeError):
        Image(os.path.join(current_dir, "0--0.jpg")).read_all()


def test_not_image_path():
    """ Should report an error. """
    with pytest.raises(RuntimeError):
        Image(os.path.join(current_dir, "__init__.py")).read_all()


def test_chinese_path():
    chinese_path = os.path.join(current_dir, "1 - 副本.jpg")
    os.link(jpg_path, chinese_path)
    _dict = {}
    try:
        i = Image(chinese_path)
        _dict = i.read_all()
    finally:
        os.remove(chinese_path)
        assert _dict


def test_read_exif():
    i = Image(img_path)
    _dict = i.read_exif()
    assert _dict["Exif.Image.DateTime"]


def test_read_iptc():
    i = Image(img_path)
    _dict = i.read_iptc()
    assert _dict["Iptc.Application2.TimeCreated"]


def test_read_xmp():
    i = Image(img_path)
    _dict = i.read_xmp()
    assert _dict["Xmp.xmp.CreateDate"]


def test_read_all():
    i = Image(img_path)
    for v in i.read_all().values():
        assert v


def test_modify_exif():
    i = Image(img_path)
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    i.modify_exif(dict1)
    _dict = i.read_exif()
    for k, v in dict1.items():
        assert v == _dict[k], "failed to set value"

    dict2 = dict1.copy()
    for k in dict2.keys():
        dict2[k] = ""
    i.modify_exif(dict2)
    _dict = i.read_exif()
    for k in dict2.keys():
        assert not _dict.get(k, None), "failed to delete key"
    i.modify_exif(dict1)


def test_modify_iptc():
    i = Image(img_path)
    dict1 = {"Iptc.Application2.ObjectName": "test-中文-",
             "Iptc.Application2.Keywords": "test-中文-"}
    i.modify_iptc(dict1)
    _dict = i.read_iptc()
    for k, v in dict1.items():
        assert v == _dict[k], "failed to set value"

    dict2 = dict1.copy()
    for k in dict2.keys():
        dict2[k] = ""
    i.modify_iptc(dict2)
    _dict = i.read_iptc()
    for k in dict2.keys():
        assert not _dict.get(k, None), "failed to delete key"
    i.modify_iptc(dict1)


def test_modify_xmp():
    i = Image(img_path)
    dict1 = {"Xmp.xmp.Rating": "5",
             "Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834"}
    i.modify_xmp(dict1)
    _dict = i.read_xmp()
    for k, v in dict1.items():
        assert v == _dict[k], "failed to set value"

    dict2 = dict1.copy()
    for k in dict2.keys():
        dict2[k] = ""
    i.modify_xmp(dict2)
    _dict = i.read_xmp()
    for k in dict2.keys():
        assert not _dict.get(k, None), "failed to delete key"
    i.modify_xmp(dict1)


