from .base import *


# First, test the most basic functionality: can it call exiv2
def test_version():
    try:
        from .base import __exiv2_version__
        assert __exiv2_version__ == '0.28.5'
    except:
        ENV.skip_test = True
        raise


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


def test_get_pixel_width():
    assert ENV.img.get_pixel_width() == data.PIXEL_WIDTH
    check_img_md5()


def test_get_pixel_height():
    assert ENV.img.get_pixel_height() == data.PIXEL_HEIGHT
    check_img_md5()


def test_get_mime_type():
    assert ENV.img.get_mime_type() == data.MIME_TYPE
    check_img_md5()


def test_get_access_mode():
    assert ENV.img.get_access_mode() == data.ACCESS_MODE
    check_img_md5()


def test_read_exif():
    diff_dict(data.EXIF, ENV.img.read_exif())
    check_img_md5()


def test_read_exif_detail():
    diff_dict(data.EXIF_DETAIL, ENV.img.read_exif_detail())
    check_img_md5()


def test_read_iptc():
    diff_dict(data.IPTC, ENV.img.read_iptc())
    check_img_md5()


def test_read_iptc_detail():
    diff_dict(data.IPTC_DETAIL, ENV.img.read_iptc_detail())
    check_img_md5()


def test_read_xmp():
    diff_dict(data.XMP, ENV.img.read_xmp())
    check_img_md5()


def test_read_xmp_detail():
    diff_dict(data.XMP_DETAIL, ENV.img.read_xmp_detail())
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


def test_read_thumbnail():
    diff_text(data.EXIF_THUMB, ENV.img.read_thumbnail())
    check_img_md5()


def test_modify_exif():
    # Test writing key and deleting key
    changes = {'Exif.Image.ImageDescription': 'test-中文-',
               'Exif.Image.Artist': None}
    ENV.img.modify_exif(changes)

    # Check the modified data
    expected_result = simulate_updating_metadata(data.EXIF, changes)
    result = ENV.img.read_exif()
    # Somehow, the value of ['Exif.Image.ExifTag', 'Exif.Thumbnail.JPEGInterchangeFormat'] will change
    ignored_keys = ['Exif.Image.ExifTag', 'Exif.Thumbnail.JPEGInterchangeFormat']
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


def test_modify_exif_all():
    ENV.img.modify_exif(data.EXIF)
    diff_dict(data.EXIF, ENV.img.read_exif())


def test_modify_iptc_all():
    ENV.img.modify_iptc(data.IPTC)
    diff_dict(data.IPTC, ENV.img.read_iptc())


def test_modify_xmp_all():
    ENV.img.modify_xmp(data.XMP)
    diff_dict(data.XMP, ENV.img.read_xmp())


def test_modify_comment():
    comment = 'Hello!  \n你好！\n' * 1000
    ENV.img.modify_comment(comment)
    diff_text(comment, ENV.img.read_comment())
    check_the_copy_of_img(diff_text, comment, 'read_comment')


def test_modify_icc():
    ENV.img.modify_icc(data.GRAY_ICC)
    diff_text(data.GRAY_ICC, ENV.img.read_icc())
    check_the_copy_of_img(diff_text, data.GRAY_ICC, 'read_icc')


def test_modify_thumbnail():
    ENV.img.modify_thumbnail(data.EXIF_THUMB)
    diff_text(data.EXIF_THUMB, ENV.img.read_thumbnail())
    check_the_copy_of_img(diff_text, data.EXIF_THUMB, 'read_thumbnail')


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


def test_clear_thumbnail():
    ENV.img.clear_thumbnail()
    diff_text(b'', ENV.img.read_thumbnail())
    check_the_copy_of_img(diff_text, b'', 'read_thumbnail')


def test_copy_to_another_image():
    try:
        shutil.copy(ENV.test_img, ENV.test_img_copy)
        with Image(ENV.test_img_copy) as img_copy:
            img_copy.clear_exif()
            img_copy.clear_iptc()
            img_copy.clear_xmp()
            img_copy.clear_comment()
            img_copy.clear_icc()
            img_copy.clear_thumbnail()
            ENV.img.copy_to_another_image(img_copy)
            diff_dict(ENV.img.read_exif()       , img_copy.read_exif())
            diff_dict(ENV.img.read_iptc()       , img_copy.read_iptc())
            diff_dict(ENV.img.read_xmp()        , img_copy.read_xmp())
            diff_text(ENV.img.read_comment()    , img_copy.read_comment())
            diff_text(ENV.img.read_icc()        , img_copy.read_icc())
            diff_text(ENV.img.read_thumbnail()  , img_copy.read_thumbnail())
    finally:
        os.remove(ENV.test_img_copy)


def test_registerNs():
    with pytest.raises(RuntimeError):
        ENV.img.modify_xmp({'Xmp.test.mytag1': 'Hello'})
    registerNs('a namespace for test', 'Ns1')
    ENV.img.modify_xmp({'Xmp.Ns1.mytag1': 'Hello'})
    assert ENV.img.read_xmp()['Xmp.Ns1.mytag1'] == 'Hello'


def test_enableBMFF():
    with Image(ENV.heic_img) as img:
        assert img.read_exif()


def test_log_level():
    with pytest.raises(RuntimeError):
        ENV.img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    set_log_level(4)
    ENV.img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    set_log_level(2)    # recover the log level
