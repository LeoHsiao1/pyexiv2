- [Tutorial](./Tutorial.md)
- [中文教程](./Tutorial-cn.md)

# 教程

## API列表

请调用`pyexiv2.Image`类的公有方法：
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

- 示例:
    ```python
    >>> from pyexiv2 import Image
    >>> i = Image(r'.\pyexiv2\tests\1.jpg')
    >>> img.read_exif()
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> img.read_iptc()
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> img.read_xmp()
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    >>> img.close()
    ```
- pyexiv2 支持包含 Unicode 字符的图片路径、元数据。默认编码格式为 utf-8 .
- 如果你不能用`utf-8`编码图片数据或路径中的中文字符，请试试用`gbk`。例如：
    ```python
    >>> img = Image(r'.\pyexiv2\tests\1 - 副本.jpg')
    RuntimeError: d:\1\pyexiv2\pyexiv2\tests\1 - 副本.jpg: Failed to open the data source: No such file or directory (errno = 2)
    >>> img = Image(r'.\pyexiv2\tests\1 - 副本.jpg', encoding='gbk')
    >>> img.close()
    ```
- 使用`Image.read_*()`是安全的。这些方法永远不会影响图片文件。（md5不变）
- 如果 XMP 元数据包含 '\v' 或 '\f'，它将被空格 ' ' 代替。
- 元数据的读取速度与元数据的数量成反比，不管图像的大小如何。


### Image.modify_*()

- 示例:
    ```python
    >>> i = Image(r'.\pyexiv2\tests\1.jpg')
    >>> # 准备要修改的XMP数据
    >>> dict1 = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',   # 这将覆盖该标签的原始值，如果不存在该标签则将其添加
    ...          'Xmp.xmp.Rating': ''}                              # 赋值一个空字符串会删除该标签
    >>> img.modify_xmp(dict1)
    >>>
    >>> dict2 = img.read_xmp()       # 检查结果
    >>> dict2['Xmp.xmp.CreateDate']
    '2019-06-23T19:45:17.834'        # 这个标签已经被修改了
    >>> dict2['Xmp.xmp.Rating']
    KeyError: 'Xmp.xmp.Rating'       # 这个标签已经被删除了
    >>> img.close()
    ```
    - 以同样的方式使用 `img.modify_exif()` 和 `img.modify_iptc()`。
- 如果你尝试修改一个非标准的标签，则可能引发一个异常。如下：
    ```python
    >>> img.modify_exif({'Exif.Image.mytag001': 'test'})    # 失败
    RuntimeError: Invalid tag name or ifdId `mytag001', ifdId 1
    >>> img.modify_xmp({'Xmp.dc.mytag001': 'test'})         # 成功
    >>> img.read_xmp()['Xmp.dc.mytag001']
    'test'
    ```
- 某些特殊的标签不能被 pyexiv2 修改。例如：
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
- 修改元数据的速度与图片的大小成反比。


### Image.clear_*()

- 调用 `img.clear_exif()` 将删除图片的所有 EXIF 元数据。一旦清除元数据，pyexiv2 可能无法完全恢复它。
  - 以同样的方式使用 `img.clear_iptc()` 和 `img.clear_xmp()` .

### Image.close()

- 当你处理完图片之后，请记得调用 `img.close()` ，以释放用于存储图像数据的内存。不调用该方法会导致内存泄漏，但不会锁定文件描述符。
- 通过 `with` 关键字打开图片时，它会自动关闭图片。例如：
    ```python
    with Image(r'.\pyexiv2\tests\1.jpg') as img:
        ims.read_exif()
    ```

## 数据类型

- 图片元数据的值可能是 Short、Long、byte、Ascii 等类型。读取时，大多数将被 pyexiv2 转换为 String 类型。
- 某些元数据是字符串列表。例如：
    ```python
    >>> img.modify_xmp({'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1', 'tag2', 'tag3']
    ```
    如果字符串中包含  `', '` ，它会被分割。如下：
    ```python
    >>> img.modify_xmp({'Xmp.dc.subject': 'tag1,tag2, tag3'})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1,tag2', 'tag3']
    ```
    你可以调用 `img.read_raw_xmp()` 以获得未分割的 XMP 元数据。

## 日志

- Exiv2 有 5 种处理日志的级别：
    - 0 : debug
    - 1 : info
    - 2 : warn
    - 3 : error
    - 4 : mute

- 默认的日志级别是 `warn` ，因此更低级别的日志不会被处理。
- `error` 日志会被转换成异常并抛出，其它日志则会被打印到 stdout 。
- 调用函数 `pyexiv2.set_log_level()` 可以设置处理日志的级别。例如：
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
