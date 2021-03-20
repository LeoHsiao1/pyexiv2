# pyexiv2

Read/Write metadata(including [EXIF](https://en.wikipedia.org/wiki/Exif), [IPTC](https://en.wikipedia.org/wiki/International_Press_Telecommunications_Council), [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform)), [comment](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md#image_comment) and [ICC Profile](https://en.wikipedia.org/wiki/ICC_profile) embedded in digital images.
- Install: `pip install pyexiv2`
- [Source code on GitHub](https://github.com/LeoHsiao1/pyexiv2)
- There was another project called [pyexiv2] (https://launchpad.net/pyexiv2), but it is based on Python2, hasn't been updated since 2011.

## Features

- Base on C++ API of [Exiv2](https://www.exiv2.org/index.html) and invoke it through [pybind11](https://github.com/pybind/pybind11).
- Supports running on Linux, MacOS and Windows, with CPython interpreter(64bit, including `3.5` `3.6` `3.7` `3.8` `3.9`).\
  If you want to run pyexiv2 on another platform, you can compile it yourself. See [pyexiv2/lib](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/lib/README.md).
- [Supports various image metadata](https://www.exiv2.org/metadata.html)
- [Supports various image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)
- Supports opening images based on the file path or from bytes data.
- Supports Unicode characters that contained in image path or metadata.

## Defects

- Can't read the image larger than 2G, or modify the image larger than 1G. ([related issue](https://github.com/Exiv2/exiv2/issues/1248))
- Not thread safe, because it uses some global variables.

## Docs

- [Tutorial](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial.md)
- [中文教程](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md)

## Tests

There are some test cases in folder [pyexiv2/tests](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/tests/).

