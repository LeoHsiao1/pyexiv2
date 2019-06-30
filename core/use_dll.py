import ctypes
import json
import os


dll_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lib")
ctypes.CDLL(os.path.join(dll_dir, "exiv2.dll"))   # import it at first
api = ctypes.CDLL(os.path.join(dll_dir, "api.dll"))


def to_char_array(s):
    """ Convert str to char array, so that can be received by C functions.
    Unicode characters need to be handled, because bytes can only contain ASCII characters. """
    return s.encode("gbk")


class metadata(dict):
    """ Store metadata in a dictionary. """
    
    def __init__(self):
        self.raw = []   # Store all the raw data
        super().__init__()


def into_dict(buffer):
    if buffer.startswith("(Caught Exiv2 exception)"):
        raise RuntimeError(buffer)
    else:
        data = metadata()
        lines = buffer.split("<<SEPARATOR>>\n")[:-1]  # the last line is empty
        for line in lines:
            # There are 3 fields: key, typeName, value
            # split with an exact count, watch out for extra '\t' in the last field
            fields = line.split('\t', 2)
            
            data.raw.append(fields)
            data[fields[0]] = fields[-1]
        return data


def read_exif(filename):
    """ return a dict """
    api.read_exif.restype = ctypes.c_char_p
    buffer = api.read_exif(to_char_array(filename))
    return into_dict(buffer.decode())


def read_iptc(filename):
    """ return a dict """
    api.read_iptc.restype = ctypes.c_char_p
    buffer = api.read_iptc(to_char_array(filename))
    return into_dict(buffer.decode())


def read_xmp(filename):
    """ return a dict """
    api.read_xmp.restype = ctypes.c_char_p
    buffer = api.read_xmp(to_char_array(filename))
    return into_dict(buffer.decode())
