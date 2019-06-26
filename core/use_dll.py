import ctypes
import json
import os


dll_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
ctypes.CDLL(os.path.join(dll_dir, "exiv2.dll"))   # import it at first
api = ctypes.CDLL(os.path.join(dll_dir, "api.dll"))


def encode(s):
    """ Unicode characters need to be handled, because bytes can only contain ASCII literal characters. """
    return s.encode("gbk")  # or "ascii"


def into_dict(buffer):
    if buffer.startswith("(Caught Exiv2 exception)"):
        raise RuntimeError(buffer)
    else:
        _dict = {}
        for line in buffer.split("<<EOL>>\n")[:-1]:
            k, v = line.split("<<;>>", 1)
            _dict[k] = v
        return _dict


def read_exif(filename):
    """ return a dict """
    api.read_exif.restype = ctypes.c_char_p
    buffer = api.read_exif(encode(filename))
    return into_dict(buffer.decode())


def read_iptc(filename):
    """ return a dict """
    api.read_iptc.restype = ctypes.c_char_p
    buffer = api.read_iptc(encode(filename))
    return into_dict(buffer.decode())


def read_xmp(filename):
    """ return a dict """
    api.read_xmp.restype = ctypes.c_char_p
    buffer = api.read_xmp(encode(filename))
    return into_dict(buffer.decode())
