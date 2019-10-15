from pyexiv2 import Image

i = Image(r"pyexiv2/tests/1.jpg")

i.read_xmp()["Xmp.dc.subject"]

d = {"Xmp.dc.subject": "flag1, flag2, flag3"}
d = {"Xmp.dc.subject": ["flag1", "flag2", "flag3"]}
i.modify_xmp(d)



import ctypes
from pyexiv2.core import api

i._open_image()
api.read_xmp.restype = ctypes.c_char_p
text = api.read_xmp().decode()
text
i._loads(text)
