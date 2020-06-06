# -*- coding: utf-8 -*-
from .base import *
from . import testdata


@check_md5
def test_read_exif():
    img = Image(path)
    compare_dict(testdata.EXIF, img.read_exif())
    img.close()


@check_md5
def test_read_iptc():
    with Image(path) as img:
        compare_dict(testdata.IPTC, img.read_iptc())


@check_md5
def test_read_xmp():
    with Image(path) as img:
        compare_dict(testdata.XMP, img.read_xmp())


@check_md5
def test_read_raw_xmp():
    with Image(path) as img:
        assert len(img.read_raw_xmp()) == 4593


def test_modify_exif():
    with Image(path) as img:
        changes = {'Exif.Image.ImageDescription': 'test-中文-',
                   'Exif.Image.Artist': ''}
        img.modify_exif(changes)
        correct_result = generate_the_correct_result(testdata.EXIF, changes)
        result = img.read_exif()
        ignored_keys = ['Exif.Image.ExifTag']
        for key in ignored_keys:
            correct_result.pop(key)
            result.pop(key)
        compare_dict(correct_result, result)


def test_modify_iptc():
    with Image(path) as img:
        changes = {'Iptc.Application2.ObjectName': 'test-中文-',
                   'Iptc.Application2.Copyright': '',
                   'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
        img.modify_iptc(changes)
        correct_result = generate_the_correct_result(testdata.IPTC, changes)
        compare_dict(correct_result, img.read_iptc())


def test_modify_xmp():
    with Image(path) as img:
        changes = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',
                   'Xmp.xmp.Rating': '',
                   'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
        img.modify_xmp(changes)
        correct_result = generate_the_correct_result(testdata.XMP, changes)
        compare_dict(correct_result, img.read_xmp())


def test_clear_exif():
    with Image(path) as img:
        img.clear_exif()
        assert img.read_exif() == {}


def test_clear_iptc():
    with Image(path) as img:
        img.clear_iptc()
        assert img.read_iptc() == {}


def test_clear_xmp():
    with Image(path) as img:
        img.clear_xmp()
        assert img.read_xmp() == {}


@check_md5
def test_nonexistent_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(current_dir, 'nonexistent.jpg')) as img:
            img.read_exif()


@check_md5
def test_not_image_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(current_dir, '__init__.py')) as img:
            img.read_exif()


@check_md5
def test_chinese_path():
    from ..lib import sys_name
    chinese_path = os.path.join(current_dir, '1 - 副本.jpg')
    shutil.copy(path, chinese_path)
    try:
        if sys_name == 'Linux':
            with Image(chinese_path, encoding='utf-8') as img:
                compare_dict(testdata.EXIF, img.read_exif())
        elif sys_name == 'Windows':
            with Image(chinese_path, encoding='gbk') as img:
                compare_dict(testdata.EXIF, img.read_exif())
    finally:
        os.remove(chinese_path)


def test_error_log():
    with Image(path) as img:
        with pytest.raises(RuntimeError):
            img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
        set_log_level(4)
        img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
        set_log_level(2)    # recover the log level
