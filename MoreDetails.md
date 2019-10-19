# More Details

- pyexiv2 supports Unicode characters that contained in image paths and metadata.
- pyexiv2 is not thread-safe, because some global variables are used to store data.
- The speed of reading metadata is inversely proportional to the amount of metadata, regardless of the size of the image. The speed of modifying metadata is inversely proportional to the size of the image.

## About data types

- The value of the metadata might be of type Short, Long, byte, Ascii, and so on. Most of them will be converted to String type by pyexiv2 when reading.
- Some of the XMP metadata is a list of strings. For example:

    ```python
    >>> i.modify_xmp({"Xmp.dc.subject": ["flag1", "flag2", "flag3"]})
    >>> i.read_xmp()["Xmp.dc.subject"]
    ['flag1', 'flag2', 'flag3']

    >>> i.modify_xmp({"Xmp.dc.subject": "flag1,flag2, 0"})
    >>> i.read_xmp()["Xmp.dc.subject"]
    ['flag1,flag2', '0']
    ```

    The principle that pyexiv2 handling this type of value is just like:

    ```python
    buffer = ', '.join(raw_value)
    value = buffer.split(', ')
    ```

    Therefore, if the raw value contains `', '` , it will be split.

    In addition, calling `i.read_raw_xmp()` will return the raw XMP metadata.

## About read_*()

- It is safe to use pyexiv2.Image.read_*(). These methods never affect image files. (md5 unchanged)
- If the metadata contains "\x1E\x1E", it will be replaced with "\x1E\x1F".
- If the XMP metadata contains '\v' or '\f', it will be replaced with space ' '.

## About modify_*()

- If you try to modify a non-standard tag, it may be rejected. Such as below.

    ```python
    >>> i.modify_exif({"Exif.Image.myflag001": "test"})       # Unallowed
    RuntimeError: (Caught Exiv2 exception) Invalid tag name or ifdId `myflag001', ifdId 1
    >>> i.modify_xmp({"Xmp.dc.myflag001": "test"})            # Allowed
    >>> i.read_xmp()["Xmp.dc.myflag001"]
    'test'
    ```

- Some special tags cannot be modified by pyexiv2. Therefore, you should check if your tag has been successfully modified.

    ```python
    >>> i.read_exif()['Exif.Image.ExifTag']
    '4860'
    >>> i.modify_exif({'Exif.Image.ExifTag': '1000'})
    >>> i.read_exif()['Exif.Image.ExifTag']
    '4860'      # Not changed

    >>> i.read_xmp()['Xmp.xmpMM.History']
    'type="Seq"'
    >>> i.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    Error: XMP Toolkit error 102: Indexing applied to non-array
    Error: Failed to encode XMP metadata.
    ```
