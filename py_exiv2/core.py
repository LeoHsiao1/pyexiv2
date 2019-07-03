# -*- coding: utf-8 -*-
import ctypes
import json
import os
import sys


dll_dir = os.path.join(os.path.dirname(__file__), "lib")

if sys.platform.startswith("linux"):
    ctypes.CDLL(os.path.join(dll_dir, "libexiv2.so"))  # import it at first
    api = ctypes.CDLL(os.path.join(dll_dir, "api.so"))
    # Unicode characters need to be handled, because char array can only contain ASCII characters.
    ENCODING = "utf-8"

elif sys.platform.startswith("win"):
    ctypes.CDLL(os.path.join(dll_dir, "exiv2.dll"))
    api = ctypes.CDLL(os.path.join(dll_dir, "api.dll"))
    ENCODING = "gbk"

else:
    raise RuntimeError("Unknown platform. This module should run on Windows or Linux systems.")

SEP = "\t"  # separator
EOL = "<<SEPARATOR>>\n"  # end of line


class Image:
    def __init__(self, filename):
        self.filename = filename.encode(ENCODING)
    
    def read_exif(self):
        self._open_image()
        return self._read_exif()
    
    def read_iptc(self):
        self._open_image()
        return self._read_iptc()

    def read_xmp(self):
        self._open_image()
        return self._read_xmp()

    def read_all(self):
        """ read all the metadata(including EXIF, IPTC, XMP). """
        self._open_image()
        _dict = {"EXIF": self._read_exif(),
                 "IPTC": self._read_iptc(),
                 "XMP": self._read_xmp()
                 }
        return _dict

    def _open_image(self):
        """ Let C++ program open an image and read its metadata,
        save as a global variable in C++ program. """
        api.open_image.restype = ctypes.c_char_p
        ret = api.open_image(self.filename).decode()
        if ret != '0':
            raise RuntimeError(ret)

    def _read_exif(self):
        """ call self._open_image() first """
        api.read_exif.restype = ctypes.c_char_p
        text = api.read_exif(self.filename).decode()
        return self._loads(text)

    def _read_iptc(self):
        """ call self._open_image() first """
        api.read_iptc.restype = ctypes.c_char_p
        text = api.read_iptc(self.filename).decode()
        return self._loads(text)

    def _read_xmp(self):
        """ call self._open_image() first """
        api.read_xmp.restype = ctypes.c_char_p
        text = api.read_xmp(self.filename).decode()
        return self._loads(text)

    def _loads(self, text):
        if text.startswith("(Caught Exiv2 exception)"):
            raise RuntimeError(text)
        # _list = []  # save all the data
        _dict = {}  # only save the key and value
        lines = text.split(EOL)[:-1]  # the last line is empty
        for line in lines:
            # There are 3 fields: key, typeName, value
            # split with an exact count, watch out for extra '\t' in the last field
            fields = line.split(SEP, 2)
            # _list.append(fields)
            _dict[fields[0]] = fields[-1]
        return _dict

    def _dumps(self, dict_):
        text = ""
        for k, v in dict_.items():
            text += k + SEP + v + EOL
        return text

    def modify_exif(self, exif_dict):
        text = self._dumps(exif_dict)
        buffer = ctypes.create_string_buffer(text.encode())
        self._open_image()
        api.modify_exif.restype = ctypes.c_char_p
        ret = api.modify_exif(buffer).decode()
        if ret != '0':
            raise RuntimeError(ret)

    def modify_iptc(self, iptc_dict):
        text = self._dumps(iptc_dict)
        buffer = ctypes.create_string_buffer(text.encode())
        self._open_image()
        api.modify_iptc.restype = ctypes.c_char_p
        ret = api.modify_iptc(buffer).decode()
        if ret != '0':
            raise RuntimeError(ret)

    def modify_xmp(self, xmp_dict):
        text = self._dumps(xmp_dict)
        buffer = ctypes.create_string_buffer(text.encode())
        self._open_image()
        api.modify_xmp.restype = ctypes.c_char_p
        ret = api.modify_xmp(buffer).decode()
        if ret != '0':
            raise RuntimeError(ret)
