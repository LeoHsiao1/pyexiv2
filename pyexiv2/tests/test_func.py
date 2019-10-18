# -*- coding: utf-8 -*-
from .common import *
from . import testdata


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
    try:
        test_read_all()
    finally:
        os.remove(chinese_path)


@check_md5
def test_read_exif():
    i = Image(path)
    d = i.read_exif()
    compare_dict(testdata.EXIF, d)


@check_md5
def test_read_iptc():
    i = Image(path)
    d = i.read_iptc()
    compare_dict(testdata.IPTC, d)


@check_md5
def test_read_xmp():
    i = Image(path)
    d = i.read_xmp()
    compare_dict(testdata.XMP, d)


@check_md5
def test_read_raw_xmp():
    i = Image(path)
    raw = i.read_raw_xmp()
    assert len(raw) == 4598


@check_md5
def test_read_all():
    i = Image(path)
    all_dict = i.read_all()
    compare_dict(testdata.EXIF, all_dict["EXIF"])
    compare_dict(testdata.IPTC, all_dict["IPTC"])
    compare_dict(testdata.XMP, all_dict["XMP"])


def test_modify_exif():
    i = Image(path)
    dict1 = {"Exif.Image.ImageDescription": "test-中文-",
             "Exif.Image.Artist": ""}
    i.modify_exif(dict1)
    dict2 = i.read_exif()
    for k, v in dict1.items():
        assert dict2.get(k, "") == v


def test_modify_iptc():
    i = Image(path)
    dict1 = {"Iptc.Application2.ObjectName": "test-中文-",
             "Iptc.Application2.Keywords": ""}
    i.modify_iptc(dict1)
    dict2 = i.read_iptc()
    for k, v in dict1.items():
        assert dict2.get(k, "") == v


def test_modify_xmp():
    i = Image(path)
    dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
             "Xmp.xmp.Rating": "",
             "Xmp.dc.subject": ["flag1", "flag2", "flag3"]}
    i.modify_xmp(dict1)
    dict2 = i.read_xmp()
    for k, v in dict1.items():
        assert dict2.get(k, "") == v


def test_modify_all():
    i = Image(path)
    all_dict = {"EXIF": {"Exif.Image.ImageDescription": "test-中文-",
                         "Exif.Image.Artist": ""},
                "IPTC": {"Iptc.Application2.ObjectName": "test-中文-",
                         "Iptc.Application2.Keywords": ""},
                "XMP": {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",
                        "Xmp.xmp.Rating": "",
                        "Xmp.dc.subject": ["flag1", "flag2", "flag3"]}
                }
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


@check_md5
def _test_recovery():
    """ a strict test, for whether it can delete testdata and recover it completely. """
    i = Image(path)
    all_dict = i.read_all()
    test_clear_all()

    # recover the testdata
    i.modify_all(all_dict)
    new_dict = i.read_all()
    for kind in all_dict.keys():
        assert len(all_dict[kind]) == len(new_dict[kind])
        for key in all_dict[kind].keys():
            assert all_dict[kind][key] == new_dict[kind][key], "{} didn't recover".format(
                key)
