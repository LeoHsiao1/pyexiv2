# pyexiv2

Read/Write metadata of digital image, including [EXIF](https://en.wikipedia.org/wiki/Exif), [IPTC](https://en.wikipedia.org/wiki/International_Press_Telecommunications_Council), [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform).

- install: `pip install pyexiv2`
- [source code on github](https://github.com/LeoHsiao1/pyexiv2)

## Features

- Runs on C++ API of [Exiv2](https://www.exiv2.org/index.html).
- Supports running on Linux and Windows, with Python3(64bit).
- [Supports various metadata](https://www.exiv2.org/metadata.html)
- [Supports various image formats](https://dev.exiv2.org/projects/exiv2/wiki/Supported_image_formats)

## Usage

read metadata :

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

modify metadata :

```python
>>> # prepare the XMP data you want to modify
>>> _dict = {"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",   # this will overwrite its original value, or add it if it doesn't exist
...          "Xmp.xmp.Rating": ""}  # set an empty str explicitly to delete the datum
>>> i.modify_xmp(_dict)
>>>
>>> xmp_dict = i.read_xmp()         # check the result
>>> xmp_dict["Xmp.xmp.CreateDate"]
'2019-06-23T19:45:17.834'           # it has been set
>>> xmp_dict["Xmp.xmp.Rating"]
KeyError: 'Xmp.xmp.Rating'          # it has been deleted
```

- Use i.modify_exif() and i.modify_iptc() in the same way.

In short, please call the public methods of class `pyexiv2.Image` :

```python
i = Image("tests/1.jpg")

i.read_exif()
i.read_iptc()
i.read_xmp()
i.read_raw_xmp()
i.read_all()

i.modify_exif({"Exif.Image.ImageDescription": "test",...})
i.modify_iptc({"Iptc.Application2.ObjectName": "test",...})
i.modify_xmp({"Xmp.xmp.CreateDate": "2019-06-23T19:45:17.834",...})
i.modify_all({"EXIF":{...}, "IPTC":{...}, "XMP":{...}})

i.clear_exif()
i.clear_iptc()
i.clear_xmp()
i.clear_all()
```

[More Details](https://github.com/LeoHsiao1/pyexiv2/blob/master/MoreDetails.md)

## Tests

There are some test cases in folder "pyexiv2/tests". Run them by pytest:

```shell
pip install pytest psutil
pytest -v
```
