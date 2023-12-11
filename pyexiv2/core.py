from .lib import exiv2api
from .convert import *
from .convert import _parse, _dumps


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

    def get_mime_type(self) -> str:
        """ Get the MIME type of the image, such as 'image/jpeg'. """
        return self.img.get_mime_type()

    def get_access_mode(self) -> dict:
        """ Get the access mode to various metadata. """
        access_modes = {0: None,
                        1: 'read',
                        2: 'write',
                        3: 'read+write'}
        dic = self.img.get_access_mode()
        dic = {k:access_modes.get(v) for k,v in dic.items()}
        return dic

    def read_exif(self, encoding='utf-8') -> dict:
        data = _parse(self.img.read_exif(), encoding)
        for tag in EXIF_TAGS_ENCODED_IN_UCS2:
            value = data.get(tag)
            if value:
                data[tag] = decode_ucs2(value)
        return data

    def read_iptc(self, encoding='utf-8') -> dict:
        data = _parse(self.img.read_iptc(), encoding)
        # For repeatable tags, the value is converted to list type even if there are no multiple values.
        for tag in IPTC_TAGS_REPEATABLE:
            value = data.get(tag)
            if isinstance(value, str):
                data[tag] = [value]
        return data

    def read_xmp(self, encoding='utf-8') -> dict:
        return _parse(self.img.read_xmp(), encoding)

    def read_raw_xmp(self, encoding='utf-8') -> str:
        return self.img.read_raw_xmp().decode(encoding)

    def read_comment(self, encoding='utf-8') -> str:
        return self.img.read_comment().decode(encoding)

    def read_icc(self) -> bytes:
        return self.img.read_icc()

    def read_thumbnail(self) -> bytes:
        return self.img.read_thumbnail()

    def modify_exif(self, data: dict, encoding='utf-8'):
        data = data.copy()  # Avoid modifying the original data
        for tag in EXIF_TAGS_ENCODED_IN_UCS2:
            value = data.get(tag)
            if value:
                data[tag] = encode_ucs2(value)
        self.img.modify_exif(_dumps(data), encoding)

    def modify_iptc(self, data: dict, encoding='utf-8'):
        self.img.modify_iptc(_dumps(data), encoding)

    def modify_xmp(self, data: dict, encoding='utf-8'):
        self.img.modify_xmp(_dumps(data), encoding)

    def modify_raw_xmp(self, data: str, encoding='utf-8'):
        self.img.modify_raw_xmp(data, encoding)

    def modify_comment(self, data: str, encoding='utf-8'):
        self.img.modify_comment(data, encoding)

    def modify_icc(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The ICC profile should be of bytes type.')
        return self.img.modify_icc(data, len(data))

    def modify_thumbnail(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The thumbnail should be of bytes type.')
        return self.img.modify_thumbnail(data, len(data))

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

    def clear_thumbnail(self):
        self.img.clear_thumbnail()


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
        return self.img.get_bytes()

    def close(self):
        """ Free the memory for storing image data. """
        self.buffer.destroy()
        super().close()


def registerNs(namespace: str, prefix: str):
    """ Register a XMP namespace with prefix. Sample:
    >>> pyexiv2.registerNs('a namespace for test', 'Ns1')
    >>> img.modify_xmp({'Xmp.Ns1.mytag1': 'Hello'})
    """
    return exiv2api.registerNs(namespace, prefix)


def enableBMFF(enable=True):
    """ Enable or disable reading BMFF images. Return True on success. """
    return exiv2api.enableBMFF(enable)


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
