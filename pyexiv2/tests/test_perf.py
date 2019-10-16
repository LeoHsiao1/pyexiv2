# -*- coding: utf-8 -*-
import psutil

from .common import *
from . import test_func


@check_md5
def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())

    for _ in range(1000):
        test_func.test_read_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        test_func.test_read_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.01, "memory leaks when reading"


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())

    for _ in range(1000):
        test_func.test_modify_all()
    m1 = p.memory_info().rss

    for _ in range(1000):
        test_func.test_modify_all()
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.01, "memory leaks when writing"


def test_stack_overflow():
    p = psutil.Process(os.getpid())
    dict1 = {"Exif.Image.ImageDescription": "(test_stack_overflow)" * 1000,
             "Exif.Image.Orientation": "0123456789"* 1000}

    for _ in range(10):
        Image(path).modify_exif(dict1)
    m1 = p.memory_info().rss

    for _ in range(10):
        Image(path).modify_exif(dict1)
    m2 = p.memory_info().rss

    assert ((m2 - m1) / m1) < 0.1, "memory leaks when writing"


def test_transfer_various_values():
    """
    Test whether various values can be transfered correctly between Python and C++ API.
    Even if a value is correctly transmitted, it does not mean that it will be successfully saved by C++ API.
    """
    import string
    from ..core import SEP, EOL, EOL_replaced
    i = Image(path)
    values = (string.digits * 5,
              string.ascii_letters * 5,
              string.punctuation * 5,
              ' \t\n\r\v \f' * 5,
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


