"""
Read and write image metadata, including EXIF, IPTC, XMP, ICC Profile.
"""


from .core import *


__version__ = '2.12.0'
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
