# pyexiv2

Read and modify metadata of digital image, including EXIF, IPTC, XMP.
It runs on C++ API of [exiv2](https://www.exiv2.org/index.html).

- install: `pip install pyexiv2`
- [source code on github](https://github.com/LeoHsiao1/pyexiv2)

## Features

- Supports running on Linux 64bit, with GLIBC_2.27.
- Supports running on Windows 64bit, with Python3(64bit).
- [Supports various metadata](https://www.exiv2.org/metadata.html)
- [Supports various image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)
- Supports Unicode characters that contained in image paths and data.
- Not thread-safe, because some global variables have been used in api.cpp.

## Usage

- read metadata

    ```python
    >>> from pyexiv2 import Image

    >>> i = Image("tests/1.jpg")
    >>> i.read_exif()
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> i.read_iptc()
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> i.read_xmp()
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    ```

- modify metadata

    ```python
    >>> # prepare the XMP data you want to modify
    >>> _dict = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",   # this will overwrite its original value, or add it if it doesn't exist
    ...          "Xmp.xmp.Rating": ""}  # set an empty str explicitly to delete the datum
    }

    >>> i.modify_xmp(_dict)
    >>> xmp_dict = i.read_xmp()         # read it again
    >>> xmp_dict["Xmp.xmp.CreateDate"]
    '2019-06-23T19:45:17.834'           # it has been set
    >>> xmp_dict["Xmp.xmp.Rating"]
    KeyError: 'Xmp.xmp.Rating'          # it has been deleted

    # use i.modify_exif() and i.modify_iptc() in the same way
    ```

- You may be interested in these metadata on Windows:

    ```python
    {'Xmp.dc.title': 'lang="x-default" I am title',
    'Xmp.dc.subject': 'label1; label2; label3',
    'Xmp.MicrosoftPhoto.Rating':'75'}
    ```

## Tests

There are some test cases in folder "pyexiv2/tests". Run them by pytest:

```shell
pip install pytest psutil
pytest -v
```
