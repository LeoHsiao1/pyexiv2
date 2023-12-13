"""
Read/Write metadata(including EXIF, IPTC, XMP), comment and ICC Profile embedded in digital images.
"""


from .core import *


__version__ = '2.9.0'
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
]
