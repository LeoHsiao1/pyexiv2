# -*- coding: utf-8 -*-
from .lib import exiv2api as api


COMMA = ', '


class Image:
    """
    This class is used for reading and writing metadata of digital image.
    Please call the public methods of this class.
    """
    
    def __init__(self, filename, encoding='utf-8'):
        """ Open an image and load its metadata. """
        self.img = api.open_image(filename.encode(encoding))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """ Free the memory for storing image data. """
        api.close_image(self.img)
        
        # Disable all public methods
        def closed_warning():
            raise RuntimeError('Do not operate on the closed image.')
        for attr in dir(self):
            if not attr.startswith('_') and callable(getattr(self, attr)):
                setattr(self, attr, closed_warning)

    def read_exif(self, encoding='utf-8') -> dict:
        self._exif = api.read_exif(self.img)
        return self._parse(self._exif, encoding)

    def read_iptc(self, encoding='utf-8') -> dict:
        self._iptc = api.read_iptc(self.img)
        return self._parse(self._iptc, encoding)

    def read_xmp(self, encoding='utf-8') -> dict:
        self._xmp = api.read_xmp(self.img)
        return self._parse(self._xmp, encoding)

    def read_raw_xmp(self, encoding='utf-8') -> str:
        self._raw_xmp = api.read_raw_xmp(self.img)
        return self._raw_xmp.decode(encoding)

    def modify_exif(self, data: dict, encoding='utf-8'):
        api.modify_exif(self.img, self._dumps(data), encoding)

    def modify_iptc(self, data: dict, encoding='utf-8'):
        api.modify_iptc(self.img, self._dumps(data), encoding)

    def modify_xmp(self, data: dict, encoding='utf-8'):
        api.modify_xmp(self.img, self._dumps(data), encoding)
    
    def _parse(self, table: list, encoding='utf-8') -> dict:
        """ Parse the table returned by C++ API into a dict. """
        data = {}
        for line in table:
            decoded_line = [i.decode(encoding) for i in line]
            key, value, typeName = decoded_line
            if typeName in ['XmpBag', 'XmpSeq']:
                value = value.split(COMMA)
            pre_value = data.get(key)
            if pre_value == None:
                data[key] = value
            elif isinstance(pre_value, str):
                data[key] = [pre_value, value]
            elif isinstance(pre_value, list):
                data[key].append(value)
        return data
    
    def _dumps(self, data: dict) -> list:
        """ Convert the metadata dict into a table that the C++ API can read. """
        table = []
        for key, value in data.items():
            typeName = 'str'
            if isinstance(value, (list, tuple)):
                typeName = 'array'
                value = COMMA.join(value)
            line = [key, value, typeName]
            table.append(line)
        return table

    def clear_exif(self):
        api.clear_exif(self.img)

    def clear_iptc(self):
        api.clear_iptc(self.img)

    def clear_xmp(self):
        api.clear_xmp(self.img)


def set_log_level(level=2):
    """
    Set the level of handling logs. There are five levels of handling logs:
        0 : debug
        1 : info
        2 : warn
        3 : error
        4 : mute
    """
    if level in [0, 1, 2, 3, 4]:
        api.set_log_level(level)
    else:
        raise ValueError('Invalid log level.')


api.init()
set_log_level(2)
