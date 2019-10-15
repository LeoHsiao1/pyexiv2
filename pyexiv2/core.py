# -*- coding: utf-8 -*-
import ctypes
import json
import os
import sys


dll_dir = os.path.join(os.path.dirname(__file__), "lib")
SEP = "\t"  # separator
EOL = "\v\f"  # use a weird symbol as EOL
EOL_replaced = "\v\b"  # If the metadata contains EOL, replace it with this symbol
EXCEPTION_HINT = "(Caught Exiv2 exception) "
OK = "OK"

# Recognize the system
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
    raise RuntimeError("Unknown platform. This module should run on Linux or Windows.")


class Image:
    """ 
    Creating an Image object just means recording the filename, not the actual operation.\n
    Please call the public methods of class Image.
    """

    def __init__(self, filename:str):
        self.filename = filename.encode(ENCODING)

    def read_exif(self) -> dict:
        self._open_image()
        return self._read_exif()

    def read_iptc(self) -> dict:
        self._open_image()
        return self._read_iptc()

    def read_xmp(self) -> dict:
        self._open_image()
        return self._read_xmp()

    def read_all(self):
        """ read all the metadata, return = {"EXIF":{...}, "IPTC":{...}, "XMP":{...}} """
        self._open_image()
        _dict = {"EXIF": self._read_exif(),
                 "IPTC": self._read_iptc(),
                 "XMP": self._read_xmp()
                 }
        return _dict

    def modify_exif(self, exif_dict):
        self._open_image()
        self._modify_exif(exif_dict)

    def modify_iptc(self, iptc_dict):
        self._open_image()
        self._modify_iptc(iptc_dict)

    def modify_xmp(self, xmp_dict):
        self._open_image()
        self._modify_xmp(xmp_dict)

    def modify_all(self, all_dict):
        """ all_dict = {"EXIF":{...}, "IPTC":{...}, "XMP":{...}} """
        self._open_image()
        self._modify_exif(all_dict["EXIF"])
        self._modify_iptc(all_dict["IPTC"])
        self._modify_xmp(all_dict["XMP"])

    def clear_exif(self):
        """ Delete all EXIF data. Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_exif()

    def clear_iptc(self):
        """ Delete all IPTC data. Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_iptc()

    def clear_xmp(self):
        """ Delete all XMP data. Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_xmp()

    def clear_all(self):
        """ Delete all the metadata. Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_exif()
        self._clear_iptc()
        self._clear_xmp()

    def _char_API_void(self, api_name):
        exec("api.{}.restype = ctypes.c_char_p".format(api_name))
        exec("ret = api.{}().decode()".format(api_name))
        exec("if ret != OK: raise RuntimeError(ret)")

    def _open_image(self):
        """ Let C++ program open an image and read its metadata,
        save as a global variable in C + +program. """
        api.open_image.restype = ctypes.c_char_p
        ret = api.open_image(self.filename).decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _read_exif(self):
        """ call self._open_image() first """
        api.read_exif.restype = ctypes.c_char_p
        text = api.read_exif().decode()
        return self._loads(text)

    def _read_iptc(self):
        """ call self._open_image() first """
        api.read_iptc.restype = ctypes.c_char_p
        text = api.read_iptc().decode()
        return self._loads(text)

    def _read_xmp(self):
        """ call self._open_image() first """
        api.read_xmp.restype = ctypes.c_char_p
        text = api.read_xmp().decode()
        return self._loads(text)

    def _modify_exif(self, exif_dict):
        text = self._dumps(exif_dict)
        buffer = ctypes.create_string_buffer(text.encode())
        api.modify_exif.restype = ctypes.c_char_p
        ret = api.modify_exif(buffer).decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _modify_iptc(self, iptc_dict):
        text = self._dumps(iptc_dict)
        buffer = ctypes.create_string_buffer(text.encode())
        api.modify_iptc.restype = ctypes.c_char_p
        ret = api.modify_iptc(buffer).decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _modify_xmp(self, xmp_dict):
        text = self._dumps(xmp_dict)
        buffer = ctypes.create_string_buffer(text.encode())
        api.modify_xmp.restype = ctypes.c_char_p
        ret = api.modify_xmp(buffer).decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _clear_exif(self):
        api.clear_exif.restype = ctypes.c_char_p
        ret = api.clear_exif().decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _clear_iptc(self):
        api.clear_iptc.restype = ctypes.c_char_p
        ret = api.clear_iptc().decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _clear_xmp(self):
        api.clear_xmp.restype = ctypes.c_char_p
        ret = api.clear_xmp().decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _loads(self, text):
        """ Parses the return value of C++ API. """
        if text.startswith(EXCEPTION_HINT):
            raise RuntimeError(text)
        _dict = {}
        lines = text.split(EOL)[:-1]  # the last line is empty
        for line in lines:
            key, typename, value = line.split(SEP, 2)
            if typename in ["XmpBag", "XmpSeq"]:
                value = value.split(',')
            _dict[key] = value
        return _dict

    def _dumps(self, _dict):
        """ Converts the metadata to a text. """
        text = ""
        for key, value in _dict.items():
            value = replace_all(value, EOL, EOL_replaced)
            if isinstance(value, (list, tuple)):
                value = ','.join(value) # convert list to str
            text += key + SEP + value + EOL
        return text


def replace_all(text, src, dest):
    result = text
    while src in result:
        result = result.replace(src, dest)
    return result

