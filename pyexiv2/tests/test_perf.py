from .base import *
from . import test_func, test_func_on_convert


def test_memory_leak_when_reading():
    process = psutil.Process(os.getpid())
    # memory_init = process.memory_info().rss
    for i in range(1000):
        if i == 1:
            memory_1 = process.memory_info().rss
        test_func.test_read_exif()
        test_func.test_read_iptc()
        test_func.test_read_xmp()
        test_func.test_read_raw_xmp()
        test_func.test_read_comment()
        test_func.test_read_icc()
        test_func_on_convert.test_convert_exif_to_xmp()
        test_func_on_convert.test_convert_iptc_to_xmp()
        test_func_on_convert.test_convert_xmp_to_exif()
        test_func_on_convert.test_convert_xmp_to_iptc()
    memory_end = process.memory_info().rss
    delta = (memory_end - memory_1) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, a memory leak may have occurred.'.format(delta)
    # If img.close() hasn't been called, the memory can increase by more than 10MB.
    check_img_md5()


def test_memory_leak_when_writing():
    process = psutil.Process(os.getpid())
    # memory_init = process.memory_info().rss
    for i in range(1000):
        if i == 1:
            memory_1 = process.memory_info().rss
        test_func.test_modify_exif()
        test_func.test_modify_iptc()
        test_func.test_modify_xmp()
        test_func.test_modify_comment()
        test_func.test_modify_icc()
    memory_end = process.memory_info().rss
    delta = (memory_end - memory_1) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, a memory leak may have occurred.'.format(delta)


def test_stack_overflow():
    changes = {'Iptc.Application2.ObjectName': 'test-中文-' * 1000,
               'Iptc.Application2.Copyright': '0123456789 hello!' * 1000,
               'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3'] * 1000}
    for _ in range(10):
        ENV.img.modify_iptc(changes)
        expected_result = simulate_updating_metadata(data.IPTC, changes)
        diff_dict(expected_result, ENV.img.read_iptc())


def test_transmit_various_characters():
    """
    Test whether various characters can be transmitted correctly between Python and C++ API.
    Even if a value is correctly transmitted, it does not mean that it will be successfully saved by C++ API.
    """
    import string
    values = [string.digits * 5,
              string.ascii_letters * 5,
              string.punctuation * 5,
              string.whitespace * 5,
              'test-中文-' * 5,
              ]
    for value in values:
        ENV.img.modify_exif({'Exif.Image.ImageDescription': value})
        assert ENV.img.read_exif().get('Exif.Image.ImageDescription') == value

        ENV.img.modify_iptc({'Iptc.Application2.ObjectName': value})
        assert ENV.img.read_iptc().get('Iptc.Application2.ObjectName') == value

        # A known problem: XMP text does not support '\v' and '\f'
        xmp_value = value.replace('\v', ' ').replace('\f', ' ')
        ENV.img.modify_xmp({'Xmp.MicrosoftPhoto.LensModel': xmp_value})
        assert ENV.img.read_xmp().get('Xmp.MicrosoftPhoto.LensModel') == xmp_value


def _test_thread_safe():
    """
    Test whether pyexiv2 can successfully run multiple threads.
    TODO: pyexiv2 is not thread-safe because in exiv2api.cpp, check_error_log() reads and writes to a global variable.
    """
    import multiprocessing
    pool = multiprocessing.Pool(3)
    for _ in range(5):
        pool.apply_async(test_memory_leak_when_reading, ())
    pool.close()
    pool.join()
