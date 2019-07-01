# easy_exiv2

This module can read and modify metadata of electronic image, including EXIF, IPTC, XMP.
It runs on C++ API of exiv2.

## Feature

- Supported platforms: Linux 64bit , Windows 64bit
- Works with Python versions from 3.4 to 3.8+??
- Support for image paths and data that contain unicode characters.
- Not thread-safe, because some global variables have been used in api.cpp.

## Usage

```python
>>> from easy_exiv2 import image

>>> i = image("core/tests/1.jpg"))  # input an image path
>>> i.read_all()    # read all the metadata(including EXIF, IPTC, XMP)
>>> i.exif_dict     # show those data right now
{'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'test-中文-', 'Exif.Image.Rating': '4', ...}
>>> i.iptc_dict
{'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'test-中文-', 'Iptc.Application2.Keywords': 'test-中文-', ...}
>>> i.xmp_dict
{'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" test-中文-', 'Xmp.dc.subject': 'test-中文-', ...}

>>> # assign the XMP data you want to modify
>>> dict1 = {"Xmp.xmp.Rating": "",
...          "Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834"}
# line 1 will delete the datum in the image, because its value is empty
# line 2 will overwrite its original value, or add it if its key doesn't exist in the image

>>> i.modify_xmp(dict1)
>>> i.read_all()    # read the metadata again
>>> i.xmp_dict["Xmp.xmp.CreateDate"]   # it has been set
'2019-06-23T19:45:17.834'
>>> i.xmp_dict["Xmp.xmp.Rating"]    # it has been deleted
KeyError: 'Xmp.xmp.Rating'

# use i.modify_exif() and i.modify_iptc() in the same way
```

## Test

There are some test cases in folder "tests". You can run them by pytest:

```shell
pip install pytest
pytest
```
