import ctypes
import json
import os


dll_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
ctypes.CDLL(os.path.join(dll_dir, "exiv2.dll"))   # import it at first
api = ctypes.CDLL(os.path.join(dll_dir, "api.dll"))


def encode(s):
    """ Unicode characters need to be handled, because bytes can only contain ASCII literal characters. """
    return s.encode("gbk")  # or "ascii"


def read_exif(filename):
    """ return a dict """

    api.exif.restype = ctypes.c_char_p
    buffer = api.exif(encode(filename))
    # api.free_buffer()     # C++ program can free the buffer automatically

    _buffer = buffer.decode()
    if _buffer.startswith("(Caught Exiv2 exception)"):
        raise RuntimeError(_buffer)
    else:
        _dict = json.loads(_buffer)
        _dict.pop("__status")
        return _dict
