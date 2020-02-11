# -*- coding: utf-8 -*-
from .common import *
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
        assert len(img.read_raw_xmp()) == 4598


def test_modify_exif():
    with Image(path) as img:
        dict1 = {"Exif.Image.ImageDescription": "test-中文-",
                "Exif.Image.Artist": ''}
        img.modify_exif(dict1)
        dict2 = img.read_exif()
        for k, v in dict1.items():
            assert dict2.get(k, '') == v


def test_modify_iptc():
    with Image(path) as img:
        dict1 = {"Iptc.Application2.ObjectName": "test-中文-",
                "Iptc.Application2.Keywords": ''}
        img.modify_iptc(dict1)
        dict2 = img.read_iptc()
        for k, v in dict1.items():
            assert dict2.get(k, '') == v


def test_modify_xmp():
    with Image(path) as img:
        dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
                "Xmp.xmp.Rating": '',
                "Xmp.dc.subject": ["flag1-中文-", "flag2-中文-", "flag3-中文-"]}
        img.modify_xmp(dict1)
        dict2 = img.read_xmp()
        for k, v in dict1.items():
            assert dict2.get(k, '') == v


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
        with Image(os.path.join(current_dir, "nonexistent.jpg")) as img:
            img.read_exif()


@check_md5
def test_not_image_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(current_dir, "__init__.py")) as img:
            img.read_exif()


@check_md5
def test_chinese_path():
    chinese_path = os.path.join(current_dir, "1 - 副本.jpg")
    shutil.copy(path, chinese_path)

    from ..lib import sys_name
    if sys_name == 'Windows':
        encoding = 'gbk'
    else:
        encoding = 'utf-8'
    
    try:
        with Image(chinese_path, encoding) as img:
            compare_dict(testdata.EXIF, img.read_exif())
    finally:
        os.remove(chinese_path)
