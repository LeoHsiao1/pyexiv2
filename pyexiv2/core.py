from .lib import exiv2api


COMMA = ', '


class Image:
    """
    Open an image based on the file path. Read and write the metadata of the image.
    Please call the public methods of this class.
    """

    def __init__(self, filename, encoding='utf-8'):
        """ Open an image and load its metadata. """
        self.img = exiv2api.Image(filename.encode(encoding))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """ Free the memory for storing image data. """
        self.img.close_image()

        # Disable all methods and properties
        def closed_warning(*args, **kwargs):
            raise RuntimeError('The image has been closed, so it is not allowed to operate.')
        for attr in dir(self):
            if not attr.startswith('__'):
                if callable(getattr(self, attr)):
                    setattr(self, attr, closed_warning)
                else:
                    setattr(self, attr, None)

    def read_exif(self, encoding='utf-8') -> dict:
        self._exif = self.img.read_exif()
        return self._parse(self._exif, encoding)

    def read_iptc(self, encoding='utf-8') -> dict:
        self._iptc = self.img.read_iptc()
        return self._parse(self._iptc, encoding)

    def read_xmp(self, encoding='utf-8') -> dict:
        self._xmp = self.img.read_xmp()
        return self._parse(self._xmp, encoding)

    def read_raw_xmp(self, encoding='utf-8') -> str:
        self._raw_xmp = self.img.read_raw_xmp()
        return self._raw_xmp.decode(encoding)

    def read_comment(self, encoding='utf-8') -> str:
        return self.img.read_comment().decode(encoding)

    def read_icc(self) -> bytes:
        return self.img.read_icc()

    def modify_exif(self, data: dict, encoding='utf-8'):
        self.img.modify_exif(self._dumps(data), encoding)

    def modify_iptc(self, data: dict, encoding='utf-8'):
        self.img.modify_iptc(self._dumps(data), encoding)

    def modify_xmp(self, data: dict, encoding='utf-8'):
        self.img.modify_xmp(self._dumps(data), encoding)

    def modify_comment(self, data: str, encoding='utf-8'):
        self.img.modify_comment(data, encoding)

    def modify_icc(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The data should be of bytes type.')
        return self.img.modify_icc(data, len(data))

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
        self.img.clear_exif()

    def clear_iptc(self):
        self.img.clear_iptc()

    def clear_xmp(self):
        self.img.clear_xmp()

    def clear_comment(self):
        self.img.clear_comment()

    def clear_icc(self):
        self.img.clear_icc()


class ImageData(Image):
    """
    Similar to class `Image`, but opens the image from bytes data.
    """
    def __init__(self, data: bytes):
        """ Open an image and load its metadata. """
        length = len(data)
        if length >= 2**31:
            raise ValueError('Only images smaller than 2GB can be opened. The size of your image is {} bytes.'.format(length))
        self.buffer = exiv2api.Buffer(data, length)
        self.img = exiv2api.Image(self.buffer)

    def get_bytes(self) -> bytes:
        """ Get the bytes data of the image. """
        return self.img.get_bytes_of_image()

    def close(self):
        """ Free the memory for storing image data. """
        self.buffer.destroy()
        super().close()


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
        exiv2api.set_log_level(level)
    else:
        raise ValueError('Invalid log level.')


exiv2api.init()
set_log_level(2)
