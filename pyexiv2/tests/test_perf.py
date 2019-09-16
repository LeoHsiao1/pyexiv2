# -*- coding: utf-8 -*-
import psutil
from .test_func import Image, os, path, jpg_path, setup_function, teardown_function, check_md5


def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())
    # m0 = p.memory_info().rss

    for _ in range(1000):
        Image(path).read_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        Image(path).read_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory leaks when reading"
    assert check_md5(path, jpg_path), "The file has been changed when reading"


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    # m0 = p.memory_info().rss

    for _ in range(1000):
        Image(path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(1000):
        Image(path).modify_exif(dict1)
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory leaks when writing"


def test_stack_overflow():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "(test_stack_overflow)" * 1000,
             "Exif.Image.Orientation": "0123456789" * 1000}
    # m0 = p.memory_info().rss

    for _ in range(10):
        Image(path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(10):
        Image(path).modify_exif(dict1)
    m2 = p.memory_info().rss

    # revert
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Orientation": "1"}
    Image(path).modify_exif(dict1)

    assert ((m2 - m1) / m1) < 0.1, "memory increasing endlessly when reading"


def _test_recover():
    """ a strict test, for whether it can delete metadata and recover it completely. """
    i = Image(path)
    all_dict = i.read_all()
    i.clear_all()
    for v in i.read_all().values():
        assert not v

    # recover the metadata
    i.modify_all(all_dict)
    new_dict = i.read_all()
    for sort in all_dict.keys():
        for key in all_dict[sort].keys():
            assert all_dict[sort][key] == new_dict[sort][key], "{} not recover".format(
                key)
