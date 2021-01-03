# -*- coding: utf-8 -*-
import psutil

from .base import *
from . import test_func


@check_md5
def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss
    for _ in range(1000):
        test_func.test_read_exif()
        test_func.test_read_iptc()
        test_func.test_read_xmp()
        test_func.test_read_raw_xmp()
    m1 = p.memory_info().rss
    delta = (m1 - m0) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, possibly due to the memory leak.'.format(delta)
    # On my machine, if img.close() hasn't been called, the memory will increase by at least 100MB.


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss
    for _ in range(1000):
        test_func.test_modify_exif()
        test_func.test_modify_iptc()
        test_func.test_modify_xmp()
    m1 = p.memory_info().rss
    delta = (m1 - m0) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, possibly due to the memory leak.'.format(delta)


def test_stack_overflow():
    with Image(test_img) as img:
        changes = {'Iptc.Application2.ObjectName': 'test-中文-' * 1000,
                   'Iptc.Application2.Copyright': '0123456789 hello!' * 1000,
                   'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3'] * 1000}
        for _ in range(10):
            img.modify_iptc(changes)
            expected_result = simulate_updating_metadata(testdata.IPTC, changes)
            diff_dict(expected_result, img.read_iptc())


def test_transmit_various_characters():
    """
    Test whether various characters can be transmitted correctly between Python and C++ API.
    Even if a value is correctly transmitted, it does not mean that it will be successfully saved by C++ API.
    """
    import string
    values = (string.digits * 5,
              string.ascii_letters * 5,
              string.punctuation * 5,
              string.whitespace * 5,
              'test-中文-' * 5,
              )
    with Image(test_img) as img:
        for v in values:
            img.modify_exif({'Exif.Image.ImageDescription': v})
            assert img.read_exif().get('Exif.Image.ImageDescription') == v

            img.modify_iptc({'Iptc.Application2.ObjectName': v})
            assert img.read_iptc().get('Iptc.Application2.ObjectName') == v

            # A known problem: XMP text does not support \v \f
            _v = v.replace('\v', ' ').replace('\f', ' ')
            img.modify_xmp({'Xmp.MicrosoftPhoto.LensModel': _v})
            assert img.read_xmp().get('Xmp.MicrosoftPhoto.LensModel') == _v


def _test_thread_safe():
    """
    Test whether pyexiv can successfully run multiple threads. 
    TODO: Could not catch the exception from the child thread.
    """
    import multiprocessing
    pool = multiprocessing.Pool(3)
    for _ in range(5):
        pool.apply_async(test_memory_leak_when_reading, ())
    pool.close()
    pool.join()


@check_md5
def _test_recovery_exif():
    """
    Test whether pyexiv2 can delete metadata and recover it completely.
    TODO: complete it
    """
    with Image(test_img) as img:
        original_dict = img.read_exif()
        img.clear_exif()
        img.modify_exif(original_dict)
        new_dict = img.read_exif()
        for key in original_dict.keys():
            for key in original_dict.keys():
                assert original_dict[key] == new_dict.get(key), "{} didn't recover".format(key)
