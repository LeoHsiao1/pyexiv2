# -*- coding: utf-8 -*-
from .common import *


@check_md5
def test_nonexistent_path():
    """ Should report an error. """
    with pytest.raises(RuntimeError):
        Image(os.path.join(current_dir, "0--0.jpg")).read_all()


@check_md5
def test_not_image_path():
    """ Should report an error. """
    with pytest.raises(RuntimeError):
        Image(os.path.join(current_dir, "__init__.py")).read_all()


@check_md5
def test_chinese_path():
    chinese_path = os.path.join(current_dir, "1 - 副本.jpg")
    shutil.copy(path, chinese_path)
    _dict = {}
    try:
        i = Image(chinese_path)
        _dict = i.read_all()
    finally:
        os.remove(chinese_path)
        assert _dict


@check_md5
def test_read_exif():
    i = Image(path)
    _dict = i.read_exif()
    assert _dict.get("Exif.Image.DateTime") == "2019:08:12 19:44:04"


@check_md5
def test_read_iptc():
    i = Image(path)
    _dict = i.read_iptc()
    assert _dict.get("Iptc.Application2.TimeCreated") == "19:44:04+00:00"


@check_md5
def test_read_xmp():
    i = Image(path)
    _dict = i.read_xmp()
    assert _dict.get("Xmp.xmp.CreateDate") == "2019-08-12T19:44:04.176"


@check_md5
def test_read_all():
    i = Image(path)
    all_dict = i.read_all()
    assert all_dict["EXIF"].get("Exif.Image.DateTime") == "2019:08:12 19:44:04"
    assert all_dict["IPTC"].get("Iptc.Application2.TimeCreated") == "19:44:04+00:00"
    assert all_dict["XMP"].get("Xmp.xmp.CreateDate") == "2019-08-12T19:44:04.176"


def test_modify_exif():
    i = Image(path)
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Artist": ""}
    i.modify_exif(dict1)
    _dict = i.read_exif()
    for k, v in dict1.items():
        assert _dict.get(k, "") == v


def test_modify_iptc():
    i = Image(path)
    dict1 = {"Iptc.Application2.ObjectName": "test-中文-",
             "Iptc.Application2.Keywords": ""}
    i.modify_iptc(dict1)
    _dict = i.read_iptc()
    for k, v in dict1.items():
        assert _dict.get(k, "") == v


def test_modify_xmp():
    i = Image(path)
    dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
             "Xmp.xmp.Rating": ""}
    i.modify_xmp(dict1)
    _dict = i.read_xmp()
    for k, v in dict1.items():
        assert _dict.get(k, "") == v


def test_modify_all():
    i = Image(path)
    all_dict = {"EXIF": {"Exif.Image.ImageDescription": "test-中文-",
                         "Exif.Image.Artist": ""},
                "IPTC": {"Iptc.Application2.ObjectName": "test-中文-",
                         "Iptc.Application2.Keywords": ""},
                "XMP": {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
                        "Xmp.xmp.Rating": ""}}
    i.modify_all(all_dict)
    new_dict = i.read_all()
    for sort in ["EXIF", "IPTC", "XMP"]:
        for k, v in all_dict[sort].items():
            assert new_dict[sort].get(k, "") == v


def test_clear_all():
    i = Image(path)
    i.clear_all()
    for v in i.read_all().values():
        assert not v
