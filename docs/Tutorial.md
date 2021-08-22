# Tutorial

Language: [English](./Tutorial.md) | [中文](./Tutorial-cn.md)

TOC:
<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Installation](#installation)
  - [FAQ](#faq)
- [API list](#api-list)
- [class Image](#class-image)
  - [close](#close)
  - [read](#read)
  - [modify](#modify)
  - [clear](#clear)
  - [comment](#comment)
  - [icc](#icc)
- [class ImageData](#class-imagedata)
- [Data types](#data-types)
- [Log](#log)
- [BMFF](#bmff)

<!-- /code_chunk_output -->

## Installation

- pyexiv2 is a third party library for Python, based on C++ and Python.
- You can execute `pip install pyexiv2` to install the compiled package of pyexiv2, which supports running on 64bit Linux, MacOS and Windows, with CPython(≥3.5) interpreter.
- If you want to run pyexiv2 on another platform, You can download the source code and compile it. See [pyexiv2/lib](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/lib/README.md).

### FAQ

- When using pyexiv2 on Linux, you may encounter the following exception:
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so'))
      self._handle = _dlopen(self._name, mode)
  OSError: /lib64/libm.so.6: version `GLIBC_2.29' not found (required by /usr/local/lib/python3.8/site-packages/pyexiv2/lib/libexiv2.so)
  ```
  - This is because pyexiv2 was compiled with GLIBC 2.29, which was released in January 2019. You need to upgrade your GLIBC library, or upgrade your Linux distribution.
  - You can execute `ldd --version` to see the version of the GLIBC library.

- When using pyexiv2 on MacOS, you may encounter the following exception:
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.dylib'))
      self._handle = _dlopen(self._name, mode)
  OSError: dlopen(/Library/Python/3.8/site-packages/pyexiv2/lib/libexiv2.dylib, 6): Library not loaded: /usr/local/lib/libintl.8.dylib
  Referenced from: /Library/Python/3.8/site-packages/pyexiv2/lib/libexiv2.dylib
  Reason: image not found
  ```
  - This is because libintl.8.dylib is missing. You need to execute `brew install gettext` .

- When using pyexiv2 on Windows, you may encounter the following exception:
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
      self._handle = _dlopen(self._name, mode)
  FileNotFoundError: Could not find module '...\lib\site-packages\pyexiv2\lib\exiv2.dll' (or one of its dependencies). Try using the full path with constructor syntax.
  ```
  - This is because the exiv2.dll file for the path does not exist, or you need to install [Microsoft Visual C++ 2015-2019](https://visualstudio.microsoft.com/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2019).

## API list

```py
class Image:
    def __init__(self, filename, encoding='utf-8')
    def close(self)
    def get_mime_type(self)
    def get_access_mode(self)

    def read_exif     (self, encoding='utf-8') -> dict
    def read_iptc     (self, encoding='utf-8') -> dict
    def read_xmp      (self, encoding='utf-8') -> dict
    def read_raw_xmp  (self, encoding='utf-8') -> str
    def read_comment  (self, encoding='utf-8') -> str
    def read_icc      (self, encoding='utf-8') -> bytes

    def modify_exif   (self, data: dict, encoding='utf-8')
    def modify_iptc   (self, data: dict, encoding='utf-8')
    def modify_xmp    (self, data: dict, encoding='utf-8')
    def modify_raw_xmp(self, data: str,  encoding='utf-8')
    def modify_comment(self, data: str,  encoding='utf-8')
    def modify_icc    (self, data: bytes)

    def clear_exif    (self)
    def clear_iptc    (self)
    def clear_xmp     (self)
    def clear_comment (self)
    def clear_icc     (self)


class ImageData(Image):
    def __init__(self, data: bytes)
    def get_bytes(self) -> bytes


def registerNs(namespace: str, prefix: str)
def enableBMFF(enable=True)
def set_log_level(level=2)
```

## class Image

- Class `Image` is used to open an image based on the file path. For example:
    ```py
    >>> import pyexiv2
    >>> img = pyexiv2.Image(r'.\pyexiv2\tests\1.jpg')
    >>> data = img.read_exif()
    >>> img.close()
    ```
- pyexiv2 supports Unicode characters that contained in image path or metadata. Most functions have a default parameter: `encoding='utf-8'`.
  - If you encounter an error because the image path or metadata contains non-ASCII characters, try changing the encoding. For example:
    ```python
    img = Image(path, encoding='utf-8')
    img = Image(path, encoding='GBK')
    img = Image(path, encoding='ISO-8859-1')
    ```
  - Another example: Windows computers in China usually encoded file paths by GBK, so they cannot be decoded by utf-8.

### close

- When you're done with the image, remember to call `img.close()` to free the memory for storing image data.
    - Not calling this method causes a memory leak, but it doesn't lock the file descriptor.
- Opening an image by keyword `with` will close the image automatically. For example:
    ```py
    with pyexiv2.Image(r'.\pyexiv2\tests\1.jpg') as img:
        data = img.read_exif()
    ```

### read

- An example of reading metadata:
    ```py
    >>> img.read_exif()
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> img.read_iptc()
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> img.read_xmp()
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    >>> img.close()
    ```
- The speed of reading metadata is inversely proportional to the amount of metadata, regardless of the size of the image.
- It is safe to call `Image.read_*()`. These methods never affect image files (md5 unchanged).
- When reading XMP metadata, the whitespace characters `\v` and `\f` are replaced with the space ` `.

### modify

- An example of modifing metadata:
    ```py
    >>> # Prepare the XMP data you want to modify
    >>> dict1 = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',   # Assign a value to a tag. This will overwrite its original value, or add it if it doesn't exist
    ...          'Xmp.xmp.Rating': None}                            # Assign None to delete the tag
    >>> img.modify_xmp(dict1)
    >>> dict2 = img.read_xmp()       # Check the result
    >>> dict2['Xmp.xmp.CreateDate']
    '2019-06-23T19:45:17.834'        # This tag has been modified
    >>> dict2['Xmp.xmp.Rating']
    KeyError: 'Xmp.xmp.Rating'       # This tag has been deleted
    >>> img.close()
    ```
    - Use `img.modify_exif()` and `img.modify_iptc()` in the same way.
- The speed of modifying metadata is inversely proportional to the size of the image.
- Modifying a non-standard tag may cause an exception. For example:
    ```py
    >>> img.modify_exif({'Exif.Image.mytag1': 'Hello'})
    RuntimeError: Invalid tag name or ifdId `mytag1', ifdId 1
    ```
    For XMP, Exiv2 supports writing non-standard XMP tags:
    ```py
    >>> img.modify_xmp({'Xmp.dc.mytag1': 'Hello'})
    >>> img.read_xmp()['Xmp.dc.mytag1']
    'Hello'
    ```
    For XMP, Exiv2 automatically registers standard namespaces and existing namespaces in the image. You can also actively register namespaces:
    ```py
    >>> img.modify_xmp({'Xmp.test.mytag1': 'Hello'})
    RuntimeError: No namespace info available for XMP prefix `test'
    >>> pyexiv2.registerNs('a namespace for test', 'Ns1')
    >>> img.modify_xmp({'Xmp.Ns1.mytag1': 'Hello'})
    >>> img.read_xmp()['Xmp.Ns1.mytag1']
    'Hello'
    ```

- Some special tags cannot be modified by pyexiv2. For example:
    ```py
    >>> img.modify_exif({'Exif.Photo.MakerNote': 'Hello'})
    >>> img.read_exif()['Exif.Photo.MakerNote']
    ''
    ```
    ```py
    >>> img.read_xmp()['Xmp.xmpMM.History']
    'type="Seq"'
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    RuntimeError: XMP Toolkit error 102: Indexing applied to non-array
    Failed to encode XMP metadata.
    ```

### clear

- Calling `img.clear_exif()` will delete all EXIF metadata of the image. Once cleared, pyexiv2 may not be able to recover it completely.
- Use `img.clear_iptc()` and `img.clear_xmp()` in the similar way.

### comment

- `img.read_comment()`、`img.modify_comment()`、`img.clear_comment()` are used to access JPEG COM (Comment) segment in the image, which does not belong to EXIF, IPTC or XMP metadata.
  - [related issue](https://github.com/Exiv2/exiv2/issues/1445)
- Sample:
    ```py
    >>> img.modify_comment('Hello World!   \n你好！\n')
    >>> img.read_comment()
    'Hello World!   \n你好！\n'
    >>> img.clear_comment()
    >>> img.read_comment()
    ''
    ```
- It can also be used to handle images that are not in JPEG format, but may have no effect or cause exceptions:
    ```py
    >>> img = pyexiv2.Image('2.gif')
    >>> img.read_comment()
    ''
    >>> img.modify_comment('Hello World!')
    RuntimeError: Setting Image comment in GIF images is not supported
    >>> img.clear_comment()
    >>> img.read_comment()
    ''
    >>> img.close()
    ```

### icc

- `img.read_icc()`、`img.modify_icc()`、`img.clear_icc()` is used to access [ICC profile](https://en.wikipedia.org/wiki/ICC_profile) in the image.

## class ImageData

- Class `ImageData`, inherited from class `Image`, is used to open an image from bytes data.
- An example of reading metadata:
    ```py
    with open(r'.\pyexiv2\tests\1.jpg', 'rb') as f:
        with pyexiv2.ImageData(f.read()) as img:
            data = img.read_exif()
    ```
- An example of modifing metadata:
    ```py
    with open(r'.\pyexiv2\tests\1.jpg', 'rb+') as f:
        with pyexiv2.ImageData(f.read()) as img:
            changes = {'Iptc.Application2.ObjectName': 'test'}
            img.modify_iptc(changes)
            # Empty the original file
            f.seek(0)
            f.truncate()
            # Get the bytes data of the image and save it to the file
            f.write(img.get_bytes())
        f.seek(0)
        with pyexiv2.ImageData(f.read()) as img:
            result = img.read_iptc()
    ```

## Data types

- The value of the metadata tag might be of type Short, Long, byte, Ascii, and so on. Most of them will be converted to String type by pyexiv2 when reading.
- Some tags has multiple values, which pyexiv2 converts to a list of strings. For example:
    ```py
    >>> img.modify_xmp({'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1', 'tag2', 'tag3']
    ```
    For these tags, pyexiv2 uses `", "` as a separator for multiple values. So it might automatically split the string you want to write. For example:
    ```py
    >>> img.modify_xmp({'Xmp.dc.subject': 'tag1,tag2, tag3'})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1,tag2', 'tag3']
    ```
- XMP tags of type LangAlt have values in multiple languages, they are converted to a dict. For example:
    ```py
    >>> img.read_xmp()['Xmp.dc.title']
    {'lang="x-default"': 'test-中文-', 'lang="de-DE"': 'Hallo, Welt'}
    ```

## BMFF

- Access to BMFF files (CR3, HEIF, HEIC, and AVIF) is disabled by default, which can be enabled by calling `pyexiv2.enableBMFF()`.
    > Attention: BMFF Support may be the subject of patent rights. pyexiv2 shall not be held responsible for identifying any such patent rights. pyexiv2 shall not be held responsible for the legal consequences of the use of this code.

## Log

- Exiv2 has five levels of handling logs：
    - 0 : debug
    - 1 : info
    - 2 : warn
    - 3 : error
    - 4 : mute

- The `error` log will be converted to an exception and thrown. Other logs will be printed to stdout.
- The default log level is `warn`, so that the lower logs will not be reported.
- Call the function `pyexiv2.set_log_level()` to set the level of handling logs. For example:
    ```py
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'}) # An error is reported
    RuntimeError: XMP Toolkit error 102: Indexing applied to non-array
    Failed to encode XMP metadata.

    >>> pyexiv2.set_log_level(4)
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'}) # No error reported
    ```
