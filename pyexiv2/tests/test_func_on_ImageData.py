import struct
import sys

from .base import *


def setup_function():
    if ENV.skip_test:
        pytest.skip()
    shutil.copy(ENV.jpg_img, ENV.test_img)  # Before each test, make a temporary copy of the image
    with open(ENV.test_img, 'rb') as f:
        ENV.img = ImageData(f.read())


def test_modify_exif():
    with open(ENV.test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Exif.Image.ImageDescription': 'test-中文-',
                       'Exif.Image.Artist': None}
            img.modify_exif(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(data.EXIF, changes)
            result = img.read_exif()
            ignored_keys = ['Exif.Image.ExifTag', 'Exif.Thumbnail.JPEGInterchangeFormat']
            for key in ignored_keys:
                expected_result.pop(key)
                result.pop(key)
            diff_dict(expected_result, result)


def test_modify_iptc():
    with open(ENV.test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Iptc.Application2.ObjectName': 'test-中文-',
                       'Iptc.Application2.Copyright': None,
                       'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
            img.modify_iptc(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(data.IPTC, changes)
            diff_dict(expected_result, img.read_iptc())


def test_modify_xmp():
    with open(ENV.test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            changes = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',
                       'Xmp.xmp.Rating': None,
                       'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
            img.modify_xmp(changes)
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            expected_result = simulate_updating_metadata(data.XMP, changes)
            diff_dict(expected_result, img.read_xmp())


def test_clear_all():
    with open(ENV.test_img, 'rb+') as f:
        with ImageData(f.read()) as img:
            img.clear_exif()
            img.clear_iptc()
            img.clear_xmp()
            img.clear_comment()
            img.clear_icc()
            img.clear_thumbnail()
            f.seek(0)
            f.write(img.get_bytes())
        f.seek(0)
        with ImageData(f.read()) as img:
            assert img.read_exif() == {}
            assert img.read_iptc() == {}
            assert img.read_xmp() == {}
            assert img.read_comment() == ''
            assert img.read_icc() == b''
            assert img.read_thumbnail() == b''


def make_tiff(description: str) -> bytes:
    """ Make a 1x1 grayscale TIFF image whose ImageDescription tag has the given value. """
    text = description.encode() + b'\0'
    text += b'\0' * (len(text) % 2)
    tags = [  # tag, type (2: ASCII, 3: SHORT, 4: LONG), count, value
        (256, 3, 1, 1),          # ImageWidth
        (257, 3, 1, 1),          # ImageLength
        (258, 3, 1, 8),          # BitsPerSample
        (259, 3, 1, 1),          # Compression
        (262, 3, 1, 1),          # PhotometricInterpretation
        (270, 2, len(text), 0),  # ImageDescription, its value is stored after the tags
        (273, 4, 1, 0),          # StripOffsets, the pixel is stored after the description
        (277, 3, 1, 1),          # SamplesPerPixel
        (278, 3, 1, 1),          # RowsPerStrip
        (279, 4, 1, 1),          # StripByteCounts
    ]
    text_offset = 8 + 2 + 12 * len(tags) + 4
    offsets = {270: text_offset, 273: text_offset + len(text)}
    ifd = struct.pack('<H', len(tags))
    for tag, tag_type, count, value in tags:
        value = offsets.get(tag, value)
        ifd += struct.pack('<HHI', tag, tag_type, count)
        ifd += struct.pack('<HH', value, 0) if tag_type == 3 else struct.pack('<I', value)
    ifd += struct.pack('<I', 0)
    return b'II*\0' + struct.pack('<I', 8) + ifd + text + b'\0'


def test_open_bytearray():
    with open(ENV.test_img, 'rb') as f:
        buf = bytearray(f.read())
    with ImageData(buf) as img:
        diff_dict(data.IPTC, img.read_iptc())
        assert img.get_bytes() == buf


def test_not_modify_input_data():
    # exiv2 updates a tag of a TIFF image in place, if the new value is not longer than the old one
    buf = make_tiff('A' * 20)
    md5 = hashlib.md5(buf).digest()
    with ImageData(buf) as img:
        assert img.read_exif()['Exif.Image.ImageDescription'] == 'A' * 20
        img.modify_exif({'Exif.Image.ImageDescription': 'B' * 20})
        result = img.get_bytes()
    assert hashlib.md5(buf).digest() == md5
    with ImageData(result) as img:
        assert img.read_exif()['Exif.Image.ImageDescription'] == 'B' * 20


def test_keep_input_data_alive():
    with open(ENV.test_img, 'rb') as f:
        img = ImageData(f.read())  # The image holds the only reference to the input data
    garbage = [bytes(os.path.getsize(ENV.test_img)) for _ in range(10)]  # Try to reuse the memory of the input data
    with open(ENV.test_img, 'rb') as f:
        assert img.get_bytes() == f.read()
    img.close()


def test_release_input_data_when_closing():
    with open(ENV.test_img, 'rb') as f:
        buf = f.read()
    img = ImageData(buf)
    refcount = sys.getrefcount(buf)
    img.close()
    assert sys.getrefcount(buf) == refcount - 1
