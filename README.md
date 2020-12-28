# pyexiv2

Read/Write metadata of digital image, including [EXIF](https://en.wikipedia.org/wiki/Exif), [IPTC](https://en.wikipedia.org/wiki/International_Press_Telecommunications_Council), [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform).

- install: `pip install pyexiv2`
- [source code on github](https://github.com/LeoHsiao1/pyexiv2)

## Features

- Base on C++ API of [Exiv2](https://www.exiv2.org/index.html) and invoke it through [pybind11](https://github.com/pybind/pybind11).
- Supports running on Linux, MacOS and Windows, with Python3(64bit, including `3.5` `3.6` `3.7` `3.8` `3.9`).
  If you want to run pyexiv2 on another platform, please compile it yourself. See [lib](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/lib/README.md)
- [Supports various metadata](https://www.exiv2.org/metadata.html)
- [Supports various image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)
- Supports opening images based on the file path or from bytes data.
- Supports Unicode characters that contained in image path or metadata.

## Defects

- Can only read the image less than 2G and modify the image less than 1G. (See https://github.com/Exiv2/exiv2/issues/1248)
- Not thread safe.

## Usage

- [Tutorial](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md)
- [中文教程](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md)

## Tests

There are some test cases in folder [pyexiv2/tests](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/tests/).

## Other notes

- Does not read/write the "JPEG COM" structure for JPEG Header comments (See https://stackoverflow.com/questions/17447201/how-do-text-comments-in-jpg-files-work )