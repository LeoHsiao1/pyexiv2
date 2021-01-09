# pyexiv2

Read/Write metadata(including [EXIF](https://en.wikipedia.org/wiki/Exif), [IPTC](https://en.wikipedia.org/wiki/International_Press_Telecommunications_Council), [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform)), comment embedded within digital images.
- Install: `pip install pyexiv2`
- [Source code on GitHub](https://github.com/LeoHsiao1/pyexiv2)

## Features

- [Supported image metadata](https://www.exiv2.org/metadata.html)
- [Supported image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)
- Base on C++ API of [Exiv2](https://www.exiv2.org/index.html) and invoke it through [pybind11](https://github.com/pybind/pybind11).
- Supports running on Linux, MacOS and Windows, with Python3(64bit, including `3.5` `3.6` `3.7` `3.8` `3.9`).
  If you want to run pyexiv2 on another platform, you can compile it yourself. See [pyexiv2/lib](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/lib/README.md)
- Supports opening images based on the file path or from bytes data.
- Supports Unicode characters that contained in image path or metadata.

## Defects

- Can't read/write image structure which is not metadata, such as DQT(Define Quantization Table).
- Can't read the image larger than 2G, and modify the image larger than 1G. [related issue](https://github.com/Exiv2/exiv2/issues/1248)
- Not thread safe, because it uses some global variables.

## Usage

- [Tutorial](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md)
- [中文教程](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md)

## Tests

There are some test cases in folder [pyexiv2/tests](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/tests/).

