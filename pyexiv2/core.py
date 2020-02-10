# -*- coding: utf-8 -*-
from .lib import api

OK = 'OK'
COMMA = ', '

class Image:
    """
    This class is used for reading and writing metadata of digital image.
    Please call the public methods of this class.
    """

    def __init__(self, filename, encoding='utf-8'):
        self.encoding = encoding
        # Open an image and load its metadata
        self.img = api.open_image(filename.encode(self.encoding))
    
    def close(self):
        api.close_image(self.img)
        def closed_warning():
            raise RuntimeError('Do not operate on the closed image.')
        for attr in dir(self):
            if not attr.startswith('_') and callable(getattr(self, attr)):
                setattr(self, attr, closed_warning)

    def read_exif(self):
        self._exif = api.read_exif(self.img)
        return self._parse(self._exif)

    def read_iptc(self):
        self._iptc = api.read_iptc(self.img)
        return self._parse(self._iptc)

    def read_xmp(self):
        self._xmp = api.read_xmp(self.img)
        return self._parse(self._xmp)

    def read_raw_xmp(self):
        self._raw_xmp = api.read_raw_xmp(self.img)
        return self._raw_xmp.decode(self.encoding)

    def modify_exif(self, _dict):
        api.modify_exif(self.img, self._dumps(_dict))

    def modify_iptc(self, _dict):
        api.modify_iptc(self.img, self._dumps(_dict))

    def modify_xmp(self, _dict):
        api.modify_xmp(self.img, self._dumps(_dict))
    
    def _parse(self, table: list) -> dict:
        """ Parse the table returned by C++ API into a dict. """
        _dict = {}
        for line in table:
            decoded_line = [i.decode(self.encoding) for i in line]
            key, value, typeName = decoded_line
            if typeName in ["XmpBag", "XmpSeq"]:
                value = value.split(COMMA)
            _dict[key] = value
        return _dict
    
    def _dumps(self, _dict) -> list:
        """ Convert the metadata dict into a table that the C++ API can read. """
        table = []
        for key, value in _dict.items():
            typeName = 'str'
            if isinstance(value, (list, tuple)):
                typeName = 'array'
                value = COMMA.join(value)
            line = [key, value, typeName]
            encoded_line = [i.encode(self.encoding) for i in line]
            table.append(encoded_line)
        return table

    def clear_exif(self):
        api.clear_exif(self.img)

    def clear_iptc(self):
        api.clear_iptc(self.img)

    def clear_xmp(self):
        api.clear_xmp(self.img)
