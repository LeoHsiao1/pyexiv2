"""
Read and write image metadata, including EXIF, IPTC, XMP, ICC Profile.
"""


from .core import *


__version__ = '2.15.1'
__exiv2_version__ = exiv2api.version()


__all__ = [
  '__version__',
  '__exiv2_version__',

  # core.py
  'Image',
  'ImageData',
  'registerNs',
  'enableBMFF',
  'set_log_level',

  # convert.py
  'convert_exif_to_xmp',
  'convert_iptc_to_xmp',
  'convert_xmp_to_exif',
  'convert_xmp_to_iptc',
]


def ImageMetadata(*args, **kwargs):
    raise NameError('ImageMetadata() is the API of py3exiv2, see https://pypi.org/project/py3exiv2 . ' +
              'However, the library you imported is pyexiv2, see https://pypi.org/project/pyexiv2 .')

