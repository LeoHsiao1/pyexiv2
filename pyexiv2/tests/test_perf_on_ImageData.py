# -*- coding: utf-8 -*-
import psutil

from .base import *
from . import test_func_on_ImageData


@check_md5
def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss
    for _ in range(1000):
        test_func_on_ImageData.test_read_all()
    m1 = p.memory_info().rss
    delta = (m1 - m0) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, possibly due to the memory leak.'.format(delta)
    # On my machine, if img.close() hasn't been called, the memory will increase by at least 100MB.


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss
    for _ in range(1000):
        test_func_on_ImageData.test_modify_exif()
        test_func_on_ImageData.test_modify_iptc()
        test_func_on_ImageData.test_modify_xmp()
    m1 = p.memory_info().rss
    delta = (m1 - m0) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, possibly due to the memory leak.'.format(delta)


def test_stack_overflow():
    for _ in range(10):
        with open(test_img, 'rb+') as f:
            with ImageData(f.read()) as img:
                changes = {'Iptc.Application2.ObjectName': 'test-中文-' * 1000,
                           'Iptc.Application2.Copyright': '0123456789 hello!' * 1000,
                           'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3'] * 1000}
                img.modify_iptc(changes)
                f.seek(0)
                f.write(img.get_bytes())
            f.seek(0)
            with ImageData(f.read()) as img:
                expected_result = simulate_updating_metadata(reference_data.IPTC, changes)
                diff_dict(expected_result, img.read_iptc())
