import os
from core.use_dll import image
import ctypes

ctypes.CDLL(r"D:\1\easy_exiv2\lib\exiv2.dll")
api = ctypes.CDLL(r"D:\1\easy_exiv2\lib\api.dll")

api.read_exif.restype = ctypes.c_char_p
b =api.read_exif(os.path.abspath(r"core\tests\1.jpg").encode())

api.write_metadata.restype = ctypes.c_char_p
api.write_metadata("Exif.Image.DateTime".encode(), "2018:06:23 19:45:17".encode())

# Exif.Image.DateTime   Ascii   2019:06:23 19:45:17

# read the metadata
i = image(os.path.abspath(r"core\tests\1.jpg"))
i.filename
i.exif_dict

# modify the dict

# .write(dict)

