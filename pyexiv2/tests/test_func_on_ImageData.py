from .base import *


@check_md5
def test_read_all():
    with open(test_img, 'rb') as f:
        with ImageData(f.read()) as img:
            diff_dict(reference.EXIF, img.read_exif())
            diff_dict(reference.IPTC, img.read_iptc())
            diff_dict(reference.XMP, img.read_xmp())
            diff_text(reference.RAW_XMP, img.read_raw_xmp())


def test_modify_exif():
    with open(test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Exif.Image.ImageDescription': 'test-中文-',
                       'Exif.Image.Artist': ''}
            img.modify_exif(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(reference.EXIF, changes)
            result = img.read_exif()
            ignored_keys = ['Exif.Image.ExifTag']
            for key in ignored_keys:
                expected_result.pop(key)
                result.pop(key)
            diff_dict(expected_result, result)


def test_modify_iptc():
    with open(test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Iptc.Application2.ObjectName': 'test-中文-',
                       'Iptc.Application2.Copyright': '',
                       'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
            img.modify_iptc(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(reference.IPTC, changes)
            diff_dict(expected_result, img.read_iptc())


def test_modify_xmp():
    with open(test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',
                       'Xmp.xmp.Rating': '',
                       'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
            img.modify_xmp(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(reference.XMP, changes)
            diff_dict(expected_result, img.read_xmp())


def test_clear_all():
    with open(test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            img.clear_exif()
            img.clear_iptc()
            img.clear_xmp()
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            assert img.read_exif() == {}
            assert img.read_iptc() == {}
            assert img.read_xmp() == {}

