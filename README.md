# py_exiv2

Read and modify metadata of digital image, including EXIF, IPTC, XMP.
It runs on C++ API of [exiv2](https://www.exiv2.org/index.html).

- install: `pip install py_exiv2`
- [source code on github](https://github.com/LeoHsiao1/py_exiv2)

## Features

- Supported platforms: Linux 64bit, Windows 64bit
- Works with Python3
- No more dependency need to be installed.
- Support for image paths and data that contain unicode characters.
- Not thread-safe, because some global variables have been used in API.

## Usage

- read metadata

    ```python
    >>> from py_exiv2 import image

    >>> i = image("tests/1.jpg")  # input an image path
    >>> i.read_all()    # read all the metadata(including EXIF, IPTC, XMP)
    >>> i.exif_dict     # show those data right now
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> i.iptc_dict
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> i.xmp_dict
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    ```

- modify metadata

    ```python
    >>> # assign the XMP data you want to modify
    >>> dict1 = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",   # overwrite its original value, or add it if its key doesn't exist in the image
    ...          "Xmp.xmp.Rating": ""}  # delete the datum in the image, because its value is empty
    }

    >>> i.modify_xmp(dict1) # do modify
    >>> i.read_all() # read the metadata again
    >>> i.xmp_dict["Xmp.xmp.CreateDate"]
    '2019-06-23T19:45:17.834' # it has been set
    >>> i.xmp_dict["Xmp.xmp.Rating"]
    KeyError: 'Xmp.xmp.Rating' # it has been deleted

    # use i.modify_exif() and i.modify_iptc() in the same way
    ```

- Metadata reference tables: <https://www.exiv2.org/metadata.html>

- The following metadata are common on Windows:

    ```python
    {'Xmp.dc.title': 'lang="x-default" I am title',
    'Xmp.dc.subject': 'flag1; flag2; flag3',
    'Xmp.MicrosoftPhoto.Rating':'75'}
    ```

## Tests

There are some test cases in folder "py_exiv2/tests". You can run them by pytest:

```shell
pip install pytest psutil
pytest -v
```
