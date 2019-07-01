import ctypes
import json
import os


dll_dir = os.path.join(os.path.dirname(__file__), "lib")
ctypes.CDLL(os.path.join(dll_dir, "exiv2.dll"))   # import it at first
api = ctypes.CDLL(os.path.join(dll_dir, "api.dll"))
SEP = "\t"  # separator
EOL = "<<SEPARATOR>>\n"  # end of line


class image:
    def __init__(self, filename):

        # Convert str to char array, so that can be received by C functions.
        # Unicode characters need to be handled, because bytes can only contain ASCII characters.
        self.filename = filename.encode("gbk")

    def read_all(self):
        """ read all the metadata(including EXIF, IPTC, XMP). """
        self._open_image()
        self._read_exif()
        self._read_iptc()
        self._read_xmp()

    def _open_image(self):
        """ Let C++ program open an image and read its metadata,
        save as a global variable in C++ program. """
        api.open_image.restype = ctypes.c_char_p
        ret = api.open_image(self.filename).decode()
        if ret != '0':
            raise RuntimeError(ret)

    def _read_exif(self):
        """ call _open_image() first """
        api.read_exif.restype = ctypes.c_char_p
        text = api.read_exif(self.filename).decode()
        self.exif_list, self.exif_dict = self._loads(text)

    def _read_iptc(self):
        """ call _open_image() first """
        api.read_iptc.restype = ctypes.c_char_p
        text = api.read_iptc(self.filename).decode()
        self.iptc_list, self.iptc_dict = self._loads(text)

    def _read_xmp(self):
        """ call _open_image() first """
        api.read_xmp.restype = ctypes.c_char_p
        text = api.read_xmp(self.filename).decode()
        self.xmp_list, self.xmp_dict = self._loads(text)

    def _loads(self, text):
        if text.startswith("(Caught Exiv2 exception)"):
            raise RuntimeError(text)
        _list = []  # save all the data
        _dict = {}  # only save the key and value
        lines = text.split(EOL)[:-1]  # the last line is empty
        for line in lines:
            # There are 3 fields: key, typeName, value
            # split with an exact count, watch out for extra '\t' in the last field
            fields = line.split(SEP, 2)
            _list.append(fields)
            _dict[fields[0]] = fields[-1]
        return _list, _dict

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
