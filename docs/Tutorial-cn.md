# 教程

语言: [English](./Tutorial.md) | [中文](./Tutorial-cn.md)

目录:
<!-- @import "[TOC]" {cmd="toc" depthFrom=2 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [安装](#安装)
  - [常见问题](#常见问题)
- [API 列表](#api-列表)
- [类 Image](#类-image)
  - [Image.read_*()](#imageread_)
  - [Image.modify_*()](#imagemodify_)
  - [Image.clear_*()](#imageclear_)
  - [Image.*_comment()](#image_comment)
- [类 ImageData](#类-imagedata)
- [数据类型](#数据类型)
- [日志](#日志)

<!-- /code_chunk_output -->

## 安装

- pyexiv2 是一个 Python 第三方库，基于 C++ 和 Python 开发。
- 你可以执行 `pip install pyexiv2` 来安装 pyexiv2 的已编译包，它支持运行在 Linux、MacOS 和 Windows 上，采用 CPython 解释器（64 bit，包括 `3.5` `3.6` `3.7` `3.8` `3.9`）。
- 如果你想在其它平台上运行 pyexiv2 ，你可以下载源代码然后编译它。参考 [pyexiv2/lib](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/lib/README.md)。

### 常见问题

- 在 Linux 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so'))
      self._handle = _dlopen(self._name, mode)
  OSError: /lib64/libm.so.6: version `GLIBC_2.29' not found (required by /usr/local/lib/python3.6/site-packages/pyexiv2/lib/libexiv2.so)
  ```
  - 这是因为 pyexiv2 在编译时使用了 GLIBC 2.29 ，它在 2019 年 1 月发布。你需要升级你的 GLIBC 库，或者升级 Linux 发行版。
  - 你可以执行 `ldd --version` 查看 GLIBC 库的版本。

- 在 Windows 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
      self._handle = _dlopen(self._name, mode)
  FileNotFoundError: Could not find module '...\lib\site-packages\pyexiv2\lib\exiv2.dll' (or one of its dependencies). Try using the full path with constructor syntax.
  ```
  - 这是因为该路径的 exiv2.dll 文件不存在，或者 Windows 电脑需要安装 [Microsoft Visual C++ Redistributable for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/#microsoft-visual-c-redistributable-for-visual-studio-2019)

## API 列表

```py
class Image:
    def __init__(self, filename, encoding='utf-8')
    def close(self)

    def read_exif(self, encoding='utf-8') -> dict
    def read_iptc(self, encoding='utf-8') -> dict
    def read_xmp(self, encoding='utf-8') -> dict
    def read_raw_xmp(self, encoding='utf-8') -> str
    def read_comment(self, encoding='utf-8') -> str
    def read_icc(self, encoding='utf-8') -> bytes

    def modify_exif(self, data: dict, encoding='utf-8')
    def modify_iptc(self, data: dict, encoding='utf-8')
    def modify_xmp(self, data: dict, encoding='utf-8')
    def modify_raw_xmp(self, data: str, encoding='utf-8')
    def modify_comment(self, data: str, encoding='utf-8')
    def modify_icc(self, data: bytes)

    def clear_exif(self)
    def clear_iptc(self)
    def clear_xmp(self)
    def clear_comment(self)
    def clear_icc(self)


class ImageData(Image):
    def __init__(self, data: bytes)
    def get_bytes(self) -> bytes


set_log_level(level=2)
```

## 类 Image

- 类 `Image` 用于根据文件路径打开图片。例如：
    ```py
    >>> import pyexiv2
    >>> img = pyexiv2.Image(r'.\pyexiv2\tests\1.jpg')
    >>> data = img.read_exif()
    >>> img.close()
    ```
- 当你处理完图片之后，请记得调用 `img.close()` ，以释放用于存储图片数据的内存。不调用该方法会导致内存泄漏，但不会锁定文件描述符。
- 通过 `with` 关键字打开图片时，它会自动关闭图片。例如：
    ```py
    with pyexiv2.Image(r'.\pyexiv2\tests\1.jpg') as img:
        data = img.read_exif()
    ```

### Image.read_*()

- 示例:
    ```py
    >>> img.read_exif()
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> img.read_iptc()
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> img.read_xmp()
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    >>> img.close()
    ```
- pyexiv2 支持包含 Unicode 字符的图片路径、元数据。大部分函数都有一个默认参数：`encoding='utf-8'`。
  如果你因为图片路径、元数据包含非 ASCII 码字符而遇到错误，请尝试更换编码。例如：
    ```python
    img = pyexiv2.Image(path, encoding='utf-8')
    img = pyexiv2.Image(path, encoding='GBK')
    img = pyexiv2.Image(path, encoding='ISO-8859-1')
    ```
   另一个例子：中国地区的 Windows 电脑通常用 GBK 编码文件路径，因此它们不能被 utf-8 解码。
- 使用 `Image.read_*()` 是安全的。这些方法永远不会影响图片文件（md5不变）。
- 如果 XMP 元数据包含 `\v` 或 `\f`，它将被空格 ` ` 代替。
- 元数据的读取速度与元数据的数量成反比，不管图片的大小如何。

### Image.modify_*()

- 示例:
    ```py
    >>> # 准备要修改的 XMP 数据
    >>> dict1 = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',   # 给一个标签赋值。这将覆盖该标签的原始值，如果不存在该标签则添加它
    ...          'Xmp.xmp.Rating': ''}                              # 赋值 None 会删除该标签
    >>> img.modify_xmp(dict1)
    >>>
    >>> dict2 = img.read_xmp()       # 检查结果
    >>> dict2['Xmp.xmp.CreateDate']
    '2019-06-23T19:45:17.834'        # 这个标签被修改了
    >>> dict2['Xmp.xmp.Rating']
    KeyError: 'Xmp.xmp.Rating'       # 这个标签被删除了
    >>> img.close()
    ```
    - `img.modify_exif()` 和 `img.modify_iptc()` 的用法同理。
- 如果你尝试修改一个非标准的标签，则可能引发一个异常。例如：
    ```py
    >>> img.modify_exif({'Exif.Image.mytag001': 'test'})    # 失败
    RuntimeError: Invalid tag name or ifdId `mytag001', ifdId 1
    >>> img.modify_xmp({'Xmp.dc.mytag001': 'test'})         # 成功
    >>> img.read_xmp()['Xmp.dc.mytag001']
    'test'
    ```
- 某些特殊的标签不能被 pyexiv2 修改。例如：
    ```py
    >>> img.modify_exif({'Exif.Photo.MakerNote': 'test'})
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
- 修改元数据的速度与图片的大小成反比。

### Image.clear_*()

- 调用 `img.clear_exif()` 将删除图片的所有 EXIF 元数据。一旦清除元数据，pyexiv2 可能无法完全恢复它。
- `img.clear_iptc()` 和 `img.clear_xmp()` 的用法同理。

### Image.*_comment()

- 它主要用于读、写 JPEG COM (COMMENT) 段，不属于 EXIF、IPTC、XMP 元数据。
  - [相关讨论](https://github.com/Exiv2/exiv2/issues/1445)
- 示例:
    ```py
    >>> img.modify_comment('Hello World!   \n你好！\n')
    >>> img.read_comment()
    'Hello World!   \n你好！\n'
    >>> img.clear_comment()
    >>> img.read_comment()
    ''
    ```
- 它也能用于处理非 JPEG 格式的图片，但可能没有效果或产生异常：
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

## 类 ImageData

- 类 `ImageData`, 继承于类 `Image`, 用于从字节数据中打开图片。
- 读取的示例：
    ```py
    with open(r'.\pyexiv2\tests\1.jpg', 'rb') as f:
        with pyexiv2.ImageData(f.read()) as img:
            data = img.read_exif()
    ```
- 修改的示例：
    ```py
    with open(r'.\pyexiv2\tests\1.jpg', 'rb+') as f:
        with pyexiv2.ImageData(f.read()) as img:
            changes = {'Iptc.Application2.ObjectName': 'test'}
            img.modify_iptc(changes)
            f.seek(0)
            # 获取图片的字节数据并保存到文件中
            f.write(img.get_bytes())
        f.seek(0)
        with pyexiv2.ImageData(f.read()) as img:
            result = img.read_iptc()
    ```

## 数据类型

- 元数据标签的值可能是 Short、Long、byte、Ascii 等类型。读取时，大多数将被 pyexiv2 转换为 String 类型。
- 某些标签有多个值，会被 pyexiv2 转换成一个字符串列表。例如：
    ```py
    >>> img.modify_xmp({'Xmp.dc.subject': ['tag1', 'tag2', 'tag3']})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1', 'tag2', 'tag3']
    ```
    对于这些标签，pyexiv2 使用 `", "` 作为多个值的分隔符。因此，它可能会自动分割你想写入的字符串。例如：
    ```py
    >>> img.modify_xmp({'Xmp.dc.subject': 'tag1,tag2, tag3'})
    >>> img.read_xmp()['Xmp.dc.subject']
    ['tag1,tag2', 'tag3']
    ```

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
    ```py
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    RuntimeError: XMP Toolkit error 102: Indexing applied to non-array
    Failed to encode XMP metadata.

    >>> pyexiv2.set_log_level(4)
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'})
    >>> img.close()
    ```
