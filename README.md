# pyexiv2

Read/Write metadata of digital image, including [EXIF](https://en.wikipedia.org/wiki/Exif), [IPTC](https://en.wikipedia.org/wiki/International_Press_Telecommunications_Council), [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform).

- install: `pip install pyexiv2`
- [source code on github](https://github.com/LeoHsiao1/pyexiv2)

## Features

- Base on C++ API of [Exiv2](https://www.exiv2.org/index.html) and [pybind11](https://github.com/pybind/pybind11).
- Supports running on Linux and Windows, with Python3(64bit, including `3.5` `3.6` `3.7` `3.8`).
- [Supports various metadata](https://www.exiv2.org/metadata.html)
- [Supports various image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)
- Supports Unicode characters that contained in image path or metadata.

## Usage

- [Tutorial](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md)
- [中文教程](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md)

## Tests

There are some test cases in folder "pyexiv2/tests". 
