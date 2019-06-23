import os
from ..use_dll import read_exif


current_dir = os.path.dirname(__file__)
jpg_path = os.path.join(current_dir, "1.jpg")
chinese_path = os.path.join(current_dir, "1 - 副本.jpg")


def test_nonexistent_file():
    """ Should report an error. """
    try:
        d = read_exif(os.path.abspath("./00.jpg"))
        assert 0
    except RuntimeError:
        pass


def test_not_pic():
    """ Should report an error. """
    try:
        d = read_exif(os.path.join(current_dir, "test_0.py"))
        assert 0
    except RuntimeError:
        pass


def test_valid_pic():
    """ Should read the metadata successfully. """
    d = read_exif(jpg_path)
    assert isinstance(d, dict)
    assert len(d)


def test_chinese_path():
    """ Now this can support Chinese path, just encode filename by "gbk". """
    d = read_exif(chinese_path)
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
        d = read_exif(jpg_path)
    m1 = p.memory_info().rss

    for _ in range(100):
        d = read_exif(jpg_path)
    m2 = p.memory_info().rss

    assert (m2 - m1) < (m1 - m0)*0.1, "memory increasing all the time"


# 测试用例：

# 图片元数据中包含中文字符时（目前可以显示。exiv2能提取Unicode字符，但是不会解码，直接显示会乱码，需要用python解码）
# 读取不存在的元数据时
# 写入不存在的元数据时
# 保存图片时，原图片被删除
