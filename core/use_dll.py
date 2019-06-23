import ctypes
import json
import os


dll_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
ctypes.CDLL(os.path.join(dll_dir, "exiv2.dll"))   # import it first
api = ctypes.CDLL(os.path.join(dll_dir, "api.dll"))


def read_exif(filename):
    """ return a dict """

    api.exif.restype = ctypes.c_char_p
    buffer = api.exif(filename.encode())
    api.free_buffer()

    _buffer = buffer.decode()
    if _buffer.startswith("(Caught Exiv2 exception)"):
        raise RuntimeError(_buffer)
    else:
        _dict = json.loads(_buffer)
        _dict.pop("__status")
        return _dict
