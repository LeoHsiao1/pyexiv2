from .base import *


def test_convert_exif_to_xmp():
    raw_data = {'Exif.Image.Artist': 'test-中文-', 'Exif.Image.Rating': '4'}
    expected_result = {'Xmp.dc.creator': ['test-中文-'], 'Xmp.xmp.Rating': '4'}
    result = convert_exif_to_xmp(raw_data)
    diff_dict(expected_result, result)

