- [Tutorial](./Tutorial.md)
- [中文教程](./Tutorial-cn.md)

# Tutorial

## API list

Please call the public methods of class `pyexiv2.Image`:
```python
class Image(filename, encoding='utf-8')
    def read_exif(self, encoding='utf-8') -> dict
    def read_iptc(self, encoding='utf-8') -> dict
    def read_xmp(self, encoding='utf-8') -> dict
    def read_raw_xmp(self, encoding='utf-8') -> str

    def modify_exif(self, dict_, encoding='utf-8')
    def modify_iptc(self, dict_, encoding='utf-8')
    def modify_xmp(self, dict_, encoding='utf-8')

    def clear_exif(self)
    def clear_iptc(self)
    def clear_xmp(self)
    
    def close(self)
```

### Image.read_*()

- Sample:
    ```python
    >>> from pyexiv2 import Image
    >>> img = Image(r'.\pyexiv2\tests\1.jpg')
    >>> img.read_exif()
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> img.read_iptc()
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> img.read_xmp()
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    >>> img.close()
    ```
- pyexiv2 supports Unicode characters that contained in image path or metadata. Most functions have a default parameter: `encoding='utf-8'`.
  If you encounter an error because the image path or metadata contains non-ASCII characters, try changing the encoding. For example:
    ```python
    img = Image(path, encoding='utf-8')
    img = Image(path, encoding='gbk')
    img = Image(path, encoding='ISO-8859-1')
    ```
  Another example: Windows computers in China usually encoded file paths by GBK, so they cannot be decoded by utf-8.
- It is safe to use `Image.read_*()`. These methods never affect image files. (md5 unchanged)
- If the XMP metadata contains '\v' or '\f', it will be replaced with space ' '.
- The speed of reading metadata is inversely proportional to the amount of metadata, regardless of the size of the image.

### Image.modify_*()

- Sample:
    ```python
    >>> img = Image(r'.\pyexiv2\tests\1.jpg')
    >>> # Prepare the XMP data you want to modify
    >>> dict1 = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',   # This will overwrite its original value, or add it if it doesn't exist
    ...          'Xmp.xmp.Rating': ''}                              # Set an empty str explicitly to delete the datum
    >>> img.modify_xmp(dict1)
    >>>
    >>> dict2 = img.read_xmp()       # Check the result
    >>> dict2['Xmp.xmp.CreateDate']
    '2019-06-23T19:45:17.834'        # This tag has been modified
    >>> dict2['Xmp.xmp.Rating']
    KeyError: 'Xmp.xmp.Rating'       # This tag has been deleted
    >>> img.close()
    ```
    - Use `img.modify_exif()` and `img.modify_iptc()` in the same way.
- If you try to modify a non-standard tag, you may cause an exception. Such as below:
    ```python
    >>> img.modify_exif({'Exif.Image.mytag001': 'test'})    # Failed
    RuntimeError: Invalid tag name or ifdId `mytag001', ifdId 1
    >>> img.modify_xmp({'Xmp.dc.mytag001': 'test'})         # Successful
    >>> img.read_xmp()['Xmp.dc.mytag001']
    'test'
    ```
- Some special tags cannot be modified by pyexiv2. For example:
    ```python
    >>> img.modify_exif({'Exif.Photo.MakerNote': 'test,,,'})
    >>> img.read_exif()['Exif.Photo.MakerNote']
    ''  
    ```
    ```python
    >>> img.read_xmp()['Xmp.xmpMM.History']
    'type="Seq"'
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    RuntimeError: XMP Toolkit error 102: Indexing applied to non-array
    Failed to encode XMP metadata.
    ```
- The speed of modifying metadata is inversely proportional to the size of the image.

### Image.clear_*()

- Calling `img.clear_exif()` will delete all EXIF metadata of the image. Once cleared, pyexiv2 may not be able to recover it completely.
  - Use `img.clear_iptc()` and `img.clear_xmp()` in the same way.

### Image.close()

- When you're done with the image, remember to call `img.close()` to free the memory for storing image data. Not calling this method causes a memory leak, but it doesn't lock the file descriptor.
- Opening an image by `with` keyword will close the image automatically. For example:
    ```python
    with Image(r'.\pyexiv2\tests\1.jpg') as img:
        ims.read_exif()
    ```

## Data types

- The value of the image metadata might be of type Short, Long, byte, Ascii, and so on. Most of them will be converted to String type by pyexiv2 when reading.
- Some metadata is a list of strings. For example:
    ```python
    >>> img.modify_xmp({'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1', 'tag2', 'tag3']
    ```
    If the string contains `', '` , it will be split. For example:
    ```python
    >>> img.modify_xmp({'Xmp.dc.subject': 'tag1,tag2, tag3'})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1,tag2', 'tag3']
    ```
    You can call `img.read_raw_xmp()` to get the raw XMP metadata without splitting.

## log

- Exiv2 has five levels of handling logs：
    - 0 : debug
    - 1 : info
    - 2 : warn
    - 3 : error
    - 4 : mute

- The default log level is `warn`, so that the lower logs will not be handled.
- The `error` log will be converted to an exception and thrown. Other logs will be printed to stdout.
- Call the function `pyexiv2.set_log_level()` to set the level of handling logs. For example:
    ```python
    >>> import pyexiv2
    >>> img = pyexiv2.Image(r'.\pyexiv2\tests\1.jpg')
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    RuntimeError: XMP Toolkit error 102: Indexing applied to non-array
    Failed to encode XMP metadata.

    >>> pyexiv2.set_log_level(4)
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    >>> img.close()
    ```
