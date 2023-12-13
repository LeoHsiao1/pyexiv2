from .base import *


def test_convert_exif_to_xmp():
    raw_data = {'Exif.Image.Artist': 'test-中文-', 'Exif.Image.Rating': '4'}
    expected_result = {'Xmp.dc.creator': ['test-中文-'], 'Xmp.xmp.Rating': '4'}
    result = convert_exif_to_xmp(raw_data)
    diff_dict(expected_result, result)


def test_convert_iptc_to_xmp():
    raw_data = {'Iptc.Application2.ObjectName': 'test-中文-', 'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
    expected_result = {'Xmp.dc.title': {'lang="x-default"': 'test-中文-'}, 'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
    result = convert_iptc_to_xmp(raw_data)
    diff_dict(expected_result, result)
