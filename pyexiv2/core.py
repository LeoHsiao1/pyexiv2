# -*- coding: utf-8 -*-
import os
import sys
import ctypes


dll_dir = os.path.join(os.path.dirname(__file__), "lib")
SEP = "\x1F"  # field separator
EOL = "\x1E\x1E"  # separator of each line
EOL_replaced = '\x1E\x1F'  # If the metadata contains EOL, replace it with this symbol
COMMA = ", "
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

    def read_raw_xmp(self) -> str:
        """ The raw XMP data is in XML format. """
        self._open_image()
        return self._read_raw_xmp()

    def read_all(self) -> dict:
        """ read all the metadata, return = {"EXIF":{...}, "IPTC":{...}, "XMP":{...}} """
        self._open_image()
        _dict = {"EXIF": self._read_exif(),
                 "IPTC": self._read_iptc(),
                 "XMP": self._read_xmp()
                 }
        return _dict

    def modify_exif(self, _dict) -> None:
        self._open_image()
        self._modify_exif(_dict)

    def modify_iptc(self, _dict) -> None:
        self._open_image()
        self._modify_iptc(_dict)

    def modify_xmp(self, _dict) -> None:
        self._open_image()
        self._modify_xmp(_dict)

    def modify_all(self, all_dict) -> None:
        """ all_dict = {"EXIF":{...}, "IPTC":{...}, "XMP":{...}} """
        self._open_image()
        self._modify_exif(all_dict["EXIF"])
        self._modify_iptc(all_dict["IPTC"])
        self._modify_xmp(all_dict["XMP"])

    def clear_exif(self) -> None:
        """ Delete all EXIF metadata.\n
        Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_exif()

    def clear_iptc(self) -> None:
        """ Delete all IPTC metadata.\n
        Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_iptc()

    def clear_xmp(self) -> None:
        """ Delete all XMP metadata.\n
        Once cleared, pyexiv2 may not be able to recover it. """
        self._open_image()
        self._clear_xmp()

    def clear_all(self) -> None:
        """ Delete all metadata of EXIF, IPTC and XMP.\n
        Once cleared, pyexiv2 may not be able to recover it. """
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
        save as a global variable in C++ program. """
        api.open_image.restype = ctypes.c_char_p
        ret = api.open_image(self.filename).decode()
        if ret != OK:
            raise RuntimeError(ret)

    def _read_exif(self):
        api.read_exif.restype = ctypes.c_char_p
        text = api.read_exif().decode()
        return self._loads(text)

    def _read_iptc(self):
        api.read_iptc.restype = ctypes.c_char_p
        text = api.read_iptc().decode()
        return self._loads(text)

    def _read_xmp(self):
        api.read_xmp.restype = ctypes.c_char_p
        text = api.read_xmp().decode()
        return self._loads(text)

    def _read_raw_xmp(self):
        api.read_raw_xmp.restype = ctypes.c_char_p
        return api.read_raw_xmp().decode()

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
        """ Parses the return text of C++ API. """
        if text.startswith(EXCEPTION_HINT):
            raise RuntimeError(text)
        _dict = {}
        lines = text.split(EOL)[:-1]  # the last line is empty
        for line in lines:
            key, typename, value = line.split(SEP, 2)
            if typename in ["XmpBag", "XmpSeq"]:
                value = value.split(COMMA)
            _dict[key] = value
        return _dict

    def _dumps(self, _dict):
        """ Converts the metadata to a text. """
        text = ""
        for key, value in _dict.items():
            typename = "str"

# TODO：把三种元数据的modify分别dumps



            if isinstance(value, (list, tuple)):
                typename = "array"
                value = COMMA.join(value) # convert list to str
            value = replace_all(value, EOL, EOL_replaced)
            text += key + SEP + typename + SEP + value + EOL
        return text


def replace_all(text:str, src: str, dest: str):
    result = text
    while src in result:
        result = result.replace(src, dest)
    return result
