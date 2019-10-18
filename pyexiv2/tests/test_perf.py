# -*- coding: utf-8 -*-
import psutil

from .common import *
from . import test_func


@check_md5
def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss

    for _ in range(1000):
        test_func.test_read_all()
    m1 = p.memory_info().rss

    delta = (m1 - m0) / 1024
    assert delta < 500, "Memory grew by {}KB, possibly due to the memory leak.".format(
        delta)


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss

    for _ in range(1000):
        test_func.test_modify_all()
    m1 = p.memory_info().rss

    delta = (m1 - m0) / 1024
    assert delta < 100, "Memory grew by {}KB, possibly due to the memory leak.".format(
        delta)


def test_stack_overflow():
    i = Image(path)
    dict1 = {"Exif.Image.ImageDescription": "(test_stack_overflow)" * 1000,
             "Exif.Image.Artist": "0123456789 hello!" * 1000}
    for _ in range(10):
        i.modify_exif(dict1)
        _dict = i.read_exif()
        for k, v in dict1.items():
            assert _dict.get(k, "") == v


def test_transmit_various_characters():
    """
    Test whether various characters can be transmitted correctly between Python and C++ API.
    Even if a value is correctly transmitted, it does not mean that it will be successfully saved by C++ API.
    """
    import string
    i = Image(path)
    values = (string.digits * 5,
              string.ascii_letters * 5,
              string.punctuation * 5,
              string.whitespace * 5,
              "test-中文-" * 5,
              )
    for v in values:
        i.modify_exif({"Exif.Image.ImageDescription": v})
        assert i.read_exif().get("Exif.Image.ImageDescription") == v

        i.modify_iptc({"Iptc.Application2.ObjectName": v})
        assert i.read_iptc().get("Iptc.Application2.ObjectName") == v

        # A known problem: XMP text does not support \v \f
        _v = v.replace('\v', ' ').replace('\f', ' ')
        i.modify_xmp({"Xmp.MicrosoftPhoto.LensModel": _v})
        assert i.read_xmp().get("Xmp.MicrosoftPhoto.LensModel") == _v
