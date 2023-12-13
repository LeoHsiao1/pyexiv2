from .base import *

EXIF = {
    'Exif.Image.Artist': 'test-中文-',
    'Exif.Image.Rating': '4',
    }
XMP_CONVERTED_FROM_EXIF = {
    'Xmp.dc.creator': ['test-中文-'],
    'Xmp.xmp.Rating': '4',
    }
IPTC = {
    'Iptc.Application2.ObjectName': 'test-中文-',
    'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3'],
    }
XMP_CONVERTED_FROM_IPTC = {
    'Xmp.dc.title': {'lang="x-default"': 'test-中文-'},
    'Xmp.dc.subject': ['tag1', 'tag2', 'tag3'],
    }


def test_convert_exif_to_xmp():
    result = convert_exif_to_xmp(EXIF)
    diff_dict(XMP_CONVERTED_FROM_EXIF, result)


def test_convert_iptc_to_xmp():
    result = convert_iptc_to_xmp(IPTC)
    diff_dict(XMP_CONVERTED_FROM_IPTC, result)


def test_convert_xmp_to_exif():
    result = convert_xmp_to_exif(XMP_CONVERTED_FROM_EXIF)
    diff_dict(EXIF, result)
