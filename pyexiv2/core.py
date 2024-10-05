from .lib import exiv2api
from .convert import *
from .convert import _parse, _parse_detail, _dumps


class Image:
    """
    Open an image based on the file path. Read and write the metadata of the image.
    Please call the public methods of this class.
    """

    def __init__(self, filename: str, encoding='utf-8'):
        """ Open an image and load its metadata. """
        self._exiv2api_image = exiv2api.Image(filename.encode(encoding))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        """ Free the memory for storing image data. """
        self._exiv2api_image.close_image()

        # Disable all methods and properties
        def closed_warning(*args, **kwargs):
            raise RuntimeError('The image has been closed, so it is not allowed to operate.')
        for attr in dir(self):
            if not attr.startswith('__'):
                if callable(getattr(self, attr)):
                    setattr(self, attr, closed_warning)
                else:
                    setattr(self, attr, None)

    def get_pixel_width(self) -> int:
        return self._exiv2api_image.get_pixel_width()

    def get_pixel_height(self) -> int:
        return self._exiv2api_image.get_pixel_height()

    def get_mime_type(self) -> str:
        """ Get the MIME type of the image, such as 'image/jpeg'. """
        return self._exiv2api_image.get_mime_type()

    def get_access_mode(self) -> dict:
        """ Get the access mode to various metadata. """
        access_modes = {0: None,
                        1: 'read',
                        2: 'write',
                        3: 'read+write'}
        dic = self._exiv2api_image.get_access_mode()
        dic = {k:access_modes.get(v) for k,v in dic.items()}
        return dic

    def read_exif(self, encoding='utf-8') -> dict:
        data = _parse(self._exiv2api_image.read_exif(), encoding)
        for tag in EXIF_TAGS_ENCODED_IN_UCS2:
            value = data.get(tag)
            if value:
                data[tag] = decode_ucs2(value)
        return data

    def read_exif_detail(self, encoding='utf-8') -> dict:
        data = _parse_detail(self._exiv2api_image.read_exif_detail(), encoding)
        for tag in EXIF_TAGS_ENCODED_IN_UCS2:
            tag_detail = data.get(tag)
            if tag_detail:
                tag_detail['value'] = decode_ucs2(tag_detail['value'])
        return data

    def read_iptc(self, encoding='utf-8') -> dict:
        data = _parse(self._exiv2api_image.read_iptc(), encoding)
        # For repeatable tags, the value is converted to list type even if there are no multiple values.
        for tag in IPTC_TAGS_REPEATABLE:
            value = data.get(tag)
            if isinstance(value, str):
                data[tag] = [value]
        return data

    def read_iptc_detail(self, encoding='utf-8') -> dict:
        data = _parse_detail(self._exiv2api_image.read_iptc_detail(), encoding)
        # For repeatable tags, the value is converted to list type even if there are no multiple values.
        for tag in IPTC_TAGS_REPEATABLE:
            tag_detail = data.get(tag)
            if tag_detail and isinstance(tag_detail['value'], str):
                tag_detail['value'] = [tag_detail['value']]
        return data

    def read_xmp(self, encoding='utf-8') -> dict:
        return _parse(self._exiv2api_image.read_xmp(), encoding)

    def read_xmp_detail(self, encoding='utf-8') -> dict:
        return _parse_detail(self._exiv2api_image.read_xmp_detail(), encoding)

    def read_raw_xmp(self, encoding='utf-8') -> str:
        return self._exiv2api_image.read_raw_xmp().decode(encoding)

    def read_comment(self, encoding='utf-8') -> str:
        return self._exiv2api_image.read_comment().decode(encoding)

    def read_icc(self) -> bytes:
        return self._exiv2api_image.read_icc()

    def read_thumbnail(self) -> bytes:
        return self._exiv2api_image.read_thumbnail()

    def modify_exif(self, data: dict, encoding='utf-8'):
        data = data.copy()  # Avoid modifying the original data when calling encode_ucs2()
        for tag in EXIF_TAGS_ENCODED_IN_UCS2:
            value = data.get(tag)
            if value:
                data[tag] = encode_ucs2(value)
        self._exiv2api_image.modify_exif(_dumps(data), encoding)

    def modify_iptc(self, data: dict, encoding='utf-8'):
        self._exiv2api_image.modify_iptc(_dumps(data), encoding)

    def modify_xmp(self, data: dict, encoding='utf-8'):
        self._exiv2api_image.modify_xmp(_dumps(data), encoding)

    def modify_raw_xmp(self, data: str, encoding='utf-8'):
        self._exiv2api_image.modify_raw_xmp(data, encoding)

    def modify_comment(self, data: str, encoding='utf-8'):
        self._exiv2api_image.modify_comment(data, encoding)

    def modify_icc(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The ICC profile should be of bytes type.')
        return self._exiv2api_image.modify_icc(data, len(data))

    def modify_thumbnail(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError('The thumbnail should be of bytes type.')
        return self._exiv2api_image.modify_thumbnail(data, len(data))

    def clear_exif(self):
        self._exiv2api_image.clear_exif()

    def clear_iptc(self):
        self._exiv2api_image.clear_iptc()

    def clear_xmp(self):
        self._exiv2api_image.clear_xmp()

    def clear_comment(self):
        self._exiv2api_image.clear_comment()

    def clear_icc(self):
        self._exiv2api_image.clear_icc()

    def clear_thumbnail(self):
        self._exiv2api_image.clear_thumbnail()

    def copy_to_another_image(self, another_image,
                              exif=True, iptc=True, xmp=True,
                              comment=True, icc=True, thumbnail=True):
        """ Copy metadata from one image to another image.
        """
        if not isinstance(another_image, (Image, ImageData)):
            raise TypeError('The type of another_image should be pyexiv2.Image or pyexiv2.ImageData.')
        self._exiv2api_image.copy_to_another_image(another_image._exiv2api_image,
                                       exif, iptc, xmp,
                                       comment, icc, thumbnail)


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
        self._exiv2api_image = exiv2api.Image(self.buffer)

    def get_bytes(self) -> bytes:
        """ Get the bytes data of the image. """
        return self._exiv2api_image.get_bytes()

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
    print('[warning] enableBMFF() is deprecated since pyexiv2 v2.14.0 . Now it is always enabled.')
    return True


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
