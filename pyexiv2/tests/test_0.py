# -*- coding: utf-8 -*-
import os

import psutil

from .. import image


current_dir = os.path.dirname(__file__)
chinese_path = os.path.join(current_dir, "1 - 副本.jpg")
jpg_path = os.path.join(current_dir, "1.jpg")


def test_nonexistent_path():
    """ Should report an error. """
    try:
        image(os.path.join(current_dir, "0--0.jpg")).read_all()
        assert 0
    except RuntimeError:
        pass


def test_not_image_path():
    """ Should report an error. """
    try:
        image(os.path.join(current_dir, "__init__.py")).read_all()
        assert 0
    except RuntimeError:
        pass


def test_chinese_path():
    i = image(chinese_path)
    i.read_all()
    assert i.exif_dict["Exif.Image.DateTime"]


def test_read_exif():
    i = image(jpg_path)
    i.read_exif()
    assert i.exif_dict["Exif.Image.DateTime"]


def test_read_iptc():
    i = image(jpg_path)
    i.read_iptc()
    assert i.iptc_dict["Iptc.Application2.TimeCreated"]


def test_read_xmp():
    i = image(jpg_path)
    i.read_xmp()
    assert i.xmp_dict["Xmp.xmp.CreateDate"]


def test_modify_exif():
    i = image(jpg_path)
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    i.modify_exif(dict1)
    i.read_all()
    for k, v in dict1.items():
        assert v == i.exif_dict[k], "failed to set value"

    dict2 = dict1.copy()
    for k in dict2.keys():
        dict2[k] = ""
    i.modify_exif(dict2)
    i.read_all()
    for k in dict2.keys():
        assert not i.exif_dict.get(k, None), "failed to delete key"
    i.modify_exif(dict1)


def test_modify_iptc():
    i = image(jpg_path)
    dict1 = {"Iptc.Application2.ObjectName": "test-中文-",
             "Iptc.Application2.Keywords": "test-中文-"}
    i.modify_iptc(dict1)
    i.read_all()
    for k, v in dict1.items():
        assert v == i.iptc_dict[k], "failed to set value"

    dict2 = dict1.copy()
    for k in dict2.keys():
        dict2[k] = ""
    i.modify_iptc(dict2)
    i.read_all()
    for k in dict2.keys():
        assert not i.iptc_dict.get(k, None), "failed to delete key"
    i.modify_iptc(dict1)


def test_modify_xmp():
    i = image(jpg_path)
    dict1 = {"Xmp.xmp.Rating": "5",
             "Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834"}
    i.modify_xmp(dict1)
    i.read_all()
    for k, v in dict1.items():
        assert v == i.xmp_dict[k], "failed to set value"

    dict2 = dict1.copy()
    for k in dict2.keys():
        dict2[k] = ""
    i.modify_xmp(dict2)
    i.read_all()
    for k in dict2.keys():
        assert not i.xmp_dict.get(k, None), "failed to delete key"
    i.modify_xmp(dict1)


def test_out_of_memory_when_reading():
    p = psutil.Process(os.getpid())
    # m0 = p.memory_info().rss

    for _ in range(1000):
        image(jpg_path).read_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        image(jpg_path).read_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory increasing all the time"


def test_out_of_memory_when_writing():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    # m0 = p.memory_info().rss

    for _ in range(1000):
        image(jpg_path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(1000):
        image(jpg_path).modify_exif(dict1)
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory increasing all the time"


def test_stack_overflow():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "(test_stack_overflow)" * 1000,
             "Exif.Image.Orientation": "0123456789"* 1000}
    # m0 = p.memory_info().rss

    for _ in range(10):
        image(jpg_path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(10):
        image(jpg_path).modify_exif(dict1)
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory increasing all the time"
