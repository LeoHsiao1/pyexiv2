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
        diff_dict(reference.EXIF, exif)
    finally:
        os.remove(chinese_path)

