from .base import *


@check_md5
def test_read_exif():
    img = Image(test_img)
    diff_dict(reference.EXIF, img.read_exif())
    img.close()


@check_md5
def test_read_iptc():
    with Image(test_img) as img:
        diff_dict(reference.IPTC, img.read_iptc())


@check_md5
def test_read_xmp():
    with Image(test_img) as img:
        diff_dict(reference.XMP, img.read_xmp())


@check_md5
def test_read_raw_xmp():
    with Image(test_img) as img:
        diff_text(reference.RAW_XMP, img.read_raw_xmp())


@check_md5
def test_read_comment():
    with Image(test_img) as img:
        diff_text(reference.COMMENT, img.read_comment())


@check_md5
def test_read_icc():
    with Image(test_img) as img:
        diff_text(reference.RGB_ICC, img.read_icc())


def test_modify_exif():
    with Image(test_img) as img:
        changes = {'Exif.Image.ImageDescription': 'test-中文-',
                   'Exif.Image.Artist': ''}
        img.modify_exif(changes)
        expected_result = simulate_updating_metadata(reference.EXIF, changes)
        result = img.read_exif()
        ignored_keys = ['Exif.Image.ExifTag']
        for key in ignored_keys:
            expected_result.pop(key)
            result.pop(key)
        diff_dict(expected_result, result)


def test_modify_iptc():
    with Image(test_img) as img:
        changes = {'Iptc.Application2.ObjectName': 'test-中文-',
                   'Iptc.Application2.Copyright': '',
                   'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
        img.modify_iptc(changes)
        expected_result = simulate_updating_metadata(reference.IPTC, changes)
        diff_dict(expected_result, img.read_iptc())


def test_modify_xmp():
    with Image(test_img) as img:
        changes = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',
                   'Xmp.xmp.Rating': '',
                   'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
        img.modify_xmp(changes)
        expected_result = simulate_updating_metadata(reference.XMP, changes)
        diff_dict(expected_result, img.read_xmp())


def test_modify_comment():
    with Image(test_img) as img:
        comment = 'Hello!  \n你好！\n' * 1000
        img.modify_comment(comment)
        diff_text(comment, img.read_comment())


def test_modify_icc():
    with Image(test_img) as img:
        img.modify_icc(reference.GRAY_ICC)
        diff_text(reference.GRAY_ICC, img.read_icc())


def test_clear_exif():
    with Image(test_img) as img:
        img.clear_exif()
        assert img.read_exif() == {}


def test_clear_iptc():
    with Image(test_img) as img:
        img.clear_iptc()
        assert img.read_iptc() == {}


def test_clear_xmp():
    with Image(test_img) as img:
        img.clear_xmp()
        assert img.read_xmp() == {}


def test_clear_comment():
    with Image(test_img) as img:
        img.clear_comment()
        assert img.read_comment() == ''


def test_clear_icc():
    with Image(test_img) as img:
        img.clear_icc()
        assert img.read_icc() == b''


@check_md5
def test_nonexistent_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(TEST_DIR, 'nonexistent.jpg')) as img:
            img.read_exif()


@check_md5
def test_not_image_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(TEST_DIR, '__init__.py')) as img:
            img.read_exif()


@check_md5
def _test_chinese_path():
    chinese_path = os.path.join(TEST_DIR, '1 - 副本.jpg')
    shutil.copy(test_img, chinese_path)
    try:
        with Image(chinese_path, encoding='utf-8') as img:
            exif = img.read_exif()
    except:
        with Image(chinese_path, encoding='gbk') as img:
            exif = img.read_exif()
        diff_dict(reference.EXIF, exif)
    finally:
        os.remove(chinese_path)


def test_error_log():
    with Image(test_img) as img:
        with pytest.raises(RuntimeError):
            img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
        set_log_level(4)
        img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
        set_log_level(2)    # recover the log level
