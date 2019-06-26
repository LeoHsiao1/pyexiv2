import os
from core.use_dll import read_exif, read_iptc, read_xmp


import ctypes

ctypes.CDLL(r"D:\1\easy_exiv2\lib\exiv2.dll")
api = ctypes.CDLL(r"D:\1\easy_exiv2\lib\api.dll")

api.read_exif.restype = ctypes.c_char_p
b =api.read_exif(os.path.abspath(r"core\tests\1.jpg").encode())




api.read_iptc.restype = ctypes.c_char_p
api.read_iptc(os.path.abspath(r"core\tests\1.jpg").encode())

api.read_xmp.restype = ctypes.c_char_p
api.read_xmp(os.path.abspath(r"core\tests\1.jpg").encode())


# read the metadata
d = read_exif(os.path.abspath(r"core\tests\1.jpg"))
for k, v in d.items():
    print(k,v)

# modify the dict

# .write(dict)

