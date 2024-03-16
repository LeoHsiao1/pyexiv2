# pyexiv2

Read/Write metadata(including [EXIF](https://en.wikipedia.org/wiki/Exif), [IPTC](https://en.wikipedia.org/wiki/International_Press_Telecommunications_Council), [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform)), [comment](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md#image_comment) and [ICC Profile](https://en.wikipedia.org/wiki/ICC_profile) embedded in digital images.
- Install: `pip install pyexiv2`
- [Source code on GitHub](https://github.com/LeoHsiao1/pyexiv2)
- [Tutorial](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md) | [中文教程](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md)

## Features

- Base on C++ API of [Exiv2](https://exiv2.org/index.html) and wrapped with [pybind11](https://github.com/pybind/pybind11).
- Supports running on 64bit Linux, MacOS and Windows, with CPython(≥3.6) interpreter.
- [Supports various image metadata](https://exiv2.org/metadata.html)
- [Supports various image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)
- Supports opening images based on the file path or from bytes data.
- Supports Unicode characters that contained in image path or metadata.

## Defects

- Can't read the image larger than 2GB, or modify the image larger than 1GB. ([related issue](https://github.com/Exiv2/exiv2/issues/1248))
- Not thread safe, because pyexiv2 uses some global variables in C++.
- Currently, if you use ARM platform, you need to compile exiv2 and pyexiv2 manually, which is troublesome. ([related issue](https://github.com/LeoHsiao1/pyexiv2/issues/108))

## Tests

There are some test cases in folder [pyexiv2/tests](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/tests/).

## References

- Similar projects:
  - [exiv2](https://exiv2.org/) is a C++ library for reading and writing various image metadata, including command-line tools.
  - [pyexiv2](https://launchpad.net/pyexiv2) is a Python2 binding to exiv2, hasn't been updated since 2011.
  - [py3exiv2](https://pypi.org/project/py3exiv2/) is a Python3 binding to exiv2, wrapped with [Boost.Python](https://boostorg.github.io/python/doc/html/index.html).
  - [python-exiv2](https://github.com/jim-easterbrook/python-exiv2) is a Python3 binding to exiv2, wrapped with [SWIG](https://swig.org/). The intention is to give direct access to all of the top-level classes in exiv2.
  - [exiftool](https://exiftool.org/) is a perl library for reading and writing various image metadata, including command-line tools.

- Books:
  - [Robin Mills. "Image Metadata and Exiv2 Architecture". 2021](https://exiv2.org/book/index.html)
