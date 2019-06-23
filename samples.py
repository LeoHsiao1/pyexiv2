import os
from core.use_dll import read_exif


import ctypes
import json

ctypes.CDLL(r"D:\1\easy_exiv2\lib\exiv2.dll")
api = ctypes.CDLL(r"D:\1\easy_exiv2\lib\api.dll")

api.free_buffer()
buffer = api.exif(os.path.abspath(r"core\tests\1.jpg").encode())





# read the metadata
d = read_exif(os.path.abspath(r"core\tests\1.jpg"))
for k, v in d.items():
    print(k,v)

# modify the dict

# .write(dict)

d = read_exif(os.path.abspath(r"core\tests\1 - 副本.jpg"))
