from .base import *


def test_open_img_by_path():
    try:
        img = Image(ENV.test_img)
        img.read_exif()
        img.close()
        check_img_md5()

        with Image(ENV.test_img) as img:
            img.read_exif()
            check_img_md5()
    except:
        ENV.skip_test = True
        raise


def test_nonexistent_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(ENV.test_dir, 'nonexistent.jpg')) as img:
            img.read_exif()


def test_not_image_path():
    with pytest.raises(RuntimeError):
        with Image(os.path.join(ENV.test_dir, '__init__.py')) as img:
            img.read_exif()


def _test_chinese_path():
    chinese_path = os.path.join(ENV.test_dir, '1 - 副本.jpg')
    shutil.copy(ENV.test_img, chinese_path)
    try:
        with Image(chinese_path, encoding='gbk') as img:
            exif = img.read_exif()
        diff_dict(data.EXIF, exif)
    finally:
        os.remove(chinese_path)


def test_read_exif():
    diff_dict(data.EXIF, ENV.img.read_exif())
    check_img_md5()


def test_read_iptc():
    diff_dict(data.IPTC, ENV.img.read_iptc())
    check_img_md5()


def test_read_xmp():
    diff_dict(data.XMP, ENV.img.read_xmp())
    check_img_md5()


def test_read_raw_xmp():
    diff_text(data.RAW_XMP, ENV.img.read_raw_xmp())
    check_img_md5()


def test_read_comment():
    diff_text(data.COMMENT, ENV.img.read_comment())
    check_img_md5()


def test_read_icc():
    diff_text(data.RGB_ICC, ENV.img.read_icc())
    check_img_md5()


def test_modify_exif():
    changes = {'Exif.Image.ImageDescription': 'test-中文-',
               'Exif.Image.Artist': None}
    ENV.img.modify_exif(changes)

    # Check the modified data
    expected_result = simulate_updating_metadata(data.EXIF, changes)
    result = ENV.img.read_exif()
    ignored_keys = ['Exif.Image.ExifTag']
    for key in ignored_keys:
        expected_result.pop(key)
        result.pop(key)
    diff_dict(expected_result, result)

    # Copy the image and check again, in case the modified data is not saved to disk
    try:
        shutil.copy(ENV.test_img, ENV.test_img_copy)
        with Image(ENV.test_img_copy) as img_copy:
            result = img_copy.read_exif()
            for key in ignored_keys:
                result.pop(key)
            diff_dict(expected_result, result)
    finally:
        os.remove(ENV.test_img_copy)


def test_modify_iptc():
    changes = {'Iptc.Application2.ObjectName': 'test-中文-',
               'Iptc.Application2.Copyright': None,
               'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3']}
    ENV.img.modify_iptc(changes)
    expected_result = simulate_updating_metadata(data.IPTC, changes)
    diff_dict(expected_result, ENV.img.read_iptc())
    check_the_copy_of_img(diff_dict, expected_result, 'read_iptc')


def test_modify_xmp():
    changes = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',
               'Xmp.xmp.Rating': None,
               'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']}
    ENV.img.modify_xmp(changes)
    expected_result = simulate_updating_metadata(data.XMP, changes)
    diff_dict(expected_result, ENV.img.read_xmp())
    check_the_copy_of_img(diff_dict, expected_result, 'read_xmp')


def test_modify_raw_xmp():
    ENV.img.clear_xmp()
    ENV.img.modify_raw_xmp(data.RAW_XMP)
    diff_text(data.RAW_XMP, ENV.img.read_raw_xmp())
    check_the_copy_of_img(diff_text, data.RAW_XMP, 'read_raw_xmp')
    test_read_xmp()


def test_modify_comment():
    comment = 'Hello!  \n你好！\n' * 1000
    ENV.img.modify_comment(comment)
    diff_text(comment, ENV.img.read_comment())
    check_the_copy_of_img(diff_text, comment, 'read_comment')


def test_modify_icc():
    ENV.img.modify_icc(data.GRAY_ICC)
    diff_text(data.GRAY_ICC, ENV.img.read_icc())
    check_the_copy_of_img(diff_text, data.GRAY_ICC, 'read_icc')


def test_clear_exif():
    ENV.img.clear_exif()
    diff_dict({}, ENV.img.read_exif())
    check_the_copy_of_img(diff_dict, {}, 'read_exif')


def test_clear_iptc():
    ENV.img.clear_iptc()
    diff_dict({}, ENV.img.read_iptc())
    check_the_copy_of_img(diff_dict, {}, 'read_iptc')


def test_clear_xmp():
    ENV.img.clear_xmp()
    diff_dict({}, ENV.img.read_xmp())
    check_the_copy_of_img(diff_dict, {}, 'read_xmp')


def test_clear_comment():
    ENV.img.clear_comment()
    diff_text('', ENV.img.read_comment())
    check_the_copy_of_img(diff_text, '', 'read_comment')


def test_clear_icc():
    ENV.img.clear_icc()
    diff_text(b'', ENV.img.read_icc())
    check_the_copy_of_img(diff_text, b'', 'read_icc')


def test_error_log():
    with pytest.raises(RuntimeError):
        ENV.img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    set_log_level(4)
    ENV.img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    set_log_level(2)    # recover the log level

