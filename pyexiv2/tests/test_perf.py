# -*- coding: utf-8 -*-
from .test_func import *


def test_out_of_memory_when_reading():
    p = psutil.Process(os.getpid())
    # m0 = p.memory_info().rss

    for _ in range(1000):
        Image(img_path).read_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        Image(img_path).read_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory increasing all the time"


def test_out_of_memory_when_writing():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    # m0 = p.memory_info().rss

    for _ in range(1000):
        Image(img_path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(1000):
        Image(img_path).modify_exif(dict1)
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory increasing all the time"


def test_stack_overflow():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "(test_stack_overflow)" * 1000,
             "Exif.Image.Orientation": "0123456789" * 1000}
    # m0 = p.memory_info().rss

    for _ in range(10):
        Image(img_path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(10):
        Image(img_path).modify_exif(dict1)
    m2 = p.memory_info().rss

    # revert
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    Image(img_path).modify_exif(dict1)

    assert ((m2 - m1) / m1) < 0.1, "memory increasing all the time"


def __test_clear_and_revert():
    i = Image(img_path)
    all_dict = i.read_all()
    i.clear_all()
    for v in i.read_all().values():  # This is also a test that reading empty data
        assert not v

    # revert the image
    i.modify_all(all_dict)
    new_dict = i.read_all()
    for sort in all_dict.keys():
        for key in all_dict[sort].keys():
            assert all_dict[sort][key] == new_dict[sort][key], "{} not reverted".format(key)
