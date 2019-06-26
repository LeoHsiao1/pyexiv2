import os
from ..use_dll import read_exif, read_iptc, read_xmp


current_dir = os.path.dirname(__file__)
chinese_path = os.path.join(current_dir, "1 - 副本.jpg")
jpg_path = os.path.join(current_dir, "1.jpg")


def test_nonexistent_path():
    """ Should report an error. """
    try:
        read_exif(os.path.join(current_dir, "0--0.jpg"))
        assert 0
    except RuntimeError:
        pass


def test_not_image_path():
    """ Should report an error. """
    try:
        read_exif(os.path.join(current_dir, "__init__.py"))
        assert 0
    except RuntimeError:
        pass


def test_chinese_path():
    """ Now this can support Chinese path, just encode filename by "gbk". """
    d = read_exif(chinese_path)
    assert isinstance(d, dict)
    assert len(d)


def test_read_exif():
    """ Should read the metadata successfully. """
    d = read_exif(jpg_path)
    assert isinstance(d, dict)
    assert len(d)


def test_read_iptc():
    """ Should read the metadata successfully. """
    d = read_iptc(jpg_path)
    assert isinstance(d, dict)
    assert len(d)


def test_read_xmp():
    """ Should read the metadata successfully. """
    d = read_xmp(jpg_path)
    assert isinstance(d, dict)
    assert len(d)


# def test_stack_overflow():
#     ...


def test_out_of_memory():
    """ Should free the buffer automatically. """
    import psutil
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss

    for _ in range(100):
        read_exif(jpg_path)
    m1 = p.memory_info().rss

    for _ in range(100):
        read_exif(jpg_path)
    m2 = p.memory_info().rss

    assert (m2 - m1) < (m1 - m0)*0.1, "memory increasing all the time"


# 测试用例：

# 图片元数据中包含中文字符时（目前可以显示。exiv2能提取Unicode字符，但是不会解码，直接显示会乱码，需要用python解码）
# 读取不存在的元数据时
# 写入不存在的元数据时
# 保存图片时，原图片被删除
# 创建几个基本测试用例，比如读取exif、iptc、xmp验证返回值不能为空，把这些基本测试用例交叉混合
