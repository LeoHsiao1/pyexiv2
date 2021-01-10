from .base import *
from . import test_func


def test_memory_leak_when_reading():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss
    for _ in range(1000):
        test_func.test_read_exif()
        test_func.test_read_iptc()
        test_func.test_read_xmp()
        test_func.test_read_raw_xmp()
        test_func.test_read_comment()
        test_func.test_read_icc()
    m1 = p.memory_info().rss
    delta = (m1 - m0) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, possibly due to the memory leak.'.format(delta)
    # If img.close() hasn't been called, the memory can increase by more than 100MB.
    check_img_md5()


def test_memory_leak_when_writing():
    p = psutil.Process(os.getpid())
    m0 = p.memory_info().rss
    for _ in range(1000):
        test_func.test_modify_exif()
        test_func.test_modify_iptc()
        test_func.test_modify_xmp()
        test_func.test_modify_comment()
        test_func.test_modify_icc()
    m1 = p.memory_info().rss
    delta = (m1 - m0) / 1024 / 1024
    assert delta < 1, 'Memory grew by {}MB, possibly due to the memory leak.'.format(delta)


def test_stack_overflow():
    changes = {'Iptc.Application2.ObjectName': 'test-中文-' * 1000,
               'Iptc.Application2.Copyright': '0123456789 hello!' * 1000,
               'Iptc.Application2.Keywords': ['tag1', 'tag2', 'tag3'] * 1000}
    for _ in range(10):
        ENV.img.modify_iptc(changes)
        expected_result = simulate_updating_metadata(reference.IPTC, changes)
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
    Test whether pyexiv can successfully run multiple threads. 
    TODO: Could not catch the exception from the child thread.
    """
    import multiprocessing
    pool = multiprocessing.Pool(3)
    for _ in range(5):
        pool.apply_async(test_memory_leak_when_reading, ())
    pool.close()
    pool.join()


def _test_recovery_exif():
    """
    Test whether pyexiv2 can delete metadata and recover it completely.
    TODO: complete it
    """
    original_dict = ENV.img.read_exif()
    ENV.img.clear_exif()
    ENV.img.modify_exif(original_dict)
    new_dict = ENV.img.read_exif()
    for key in original_dict.keys():
        for key in original_dict.keys():
            assert original_dict[key] == new_dict.get(key), "{} didn't recover".format(key)
    check_img_md5()
