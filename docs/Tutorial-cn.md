# 教程

语言: [English](./Tutorial.md) | [中文](./Tutorial-cn.md)

## 安装

- pyexiv2 是一个 Python 第三方库，基于 C++ 和 Python 开发。
- 你可以执行 `pip install pyexiv2` 来安装 pyexiv2 。它包含一些已编译的库文件，带有以下兼容条件：
  - 操作系统为 Linux、MacOS 或 Windows
  - CPU 架构为 AMD64
  - Python 解释器为 CPython(≥3.6)
- 如果你想在其它平台上运行 pyexiv2 ，你可以下载源代码然后编译它。参考 [pyexiv2/lib](https://github.com/LeoHsiao1/pyexiv2/blob/master/pyexiv2/lib/README.md)。

### 常见问题

- 在 Linux 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so'))
      self._handle = _dlopen(self._name, mode)
  OSError: /lib64/libm.so.6: version `GLIBC_2.32' not found (required by /usr/local/lib/python3.6/site-packages/pyexiv2/lib/libexiv2.so)
  ```
  - 这是因为 pyexiv2 是使用较新版本的 GLIBC 库编译的。你需要升级你的 GLIBC 库，或者升级你的 Linux 发行版。
  - 你可以在自己电脑上执行 `ldd --version` 查看 GLIBC 库的版本。

- 在 MacOS 上使用 pyexiv2 时，你可能遇到以下异常：
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
  - 这是因为 libintl.8.dylib 不存在。你需要执行 `brew install gettext` 。

- 在 MacOS 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  Library not loaded: '/usr/local/opt/inih/lib/libinih.0.dylib'
  ```
  - 这是因为 libinih.0.dylib 不存在。你需要执行 `brew install inih` 。

- 在 Windows 上使用 pyexiv2 时，你可能遇到以下异常：
  ```py
  >>> import pyexiv2
  Traceback (most recent call last):
      ...
      ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
      self._handle = _dlopen(self._name, mode)
  FileNotFoundError: Could not find module '...\lib\site-packages\pyexiv2\lib\exiv2.dll' (or one of its dependencies). Try using the full path with constructor syntax.
  ```
  - 这是因为 exiv2.dll 文件不存在，或者你需要安装 [Microsoft Visual C++ Redistributable for Visual Studio 2022](https://visualstudio.microsoft.com/downloads/) 才能识别该文件。

## API 列表

```py
class Image:
    def __init__(self, filename, encoding='utf-8')
    def close(self)

    def get_pixel_width (self) -> int
    def get_pixel_height(self) -> int
    def get_mime_type   (self) -> str
    def get_access_mode (self) -> dict

    def read_exif       (self, encoding='utf-8') -> dict
    def read_exif_detail(self, encoding='utf-8') -> dict
    def read_iptc       (self, encoding='utf-8') -> dict
    def read_iptc_detail(self, encoding='utf-8') -> dict
    def read_xmp        (self, encoding='utf-8') -> dict
    def read_xmp_detail (self, encoding='utf-8') -> dict
    def read_raw_xmp    (self, encoding='utf-8') -> str
    def read_comment    (self, encoding='utf-8') -> str
    def read_icc        (self) -> bytes
    def read_thumbnail  (self) -> bytes

    def modify_exif     (self, data: dict, encoding='utf-8')
    def modify_iptc     (self, data: dict, encoding='utf-8')
    def modify_xmp      (self, data: dict, encoding='utf-8')
    def modify_raw_xmp  (self, data: str,  encoding='utf-8')
    def modify_comment  (self, data: str,  encoding='utf-8')
    def modify_icc      (self, data: bytes)
    def modify_thumbnail(self, data: bytes)

    def clear_exif      (self)
    def clear_iptc      (self)
    def clear_xmp       (self)
    def clear_comment   (self)
    def clear_icc       (self)
    def clear_thumbnail (self)

    def copy_to_another_image(self, another_image,
                              exif=True, iptc=True, xmp=True,
                              comment=True, icc=True, thumbnail=True)


class ImageData(Image):
    def __init__(self, data: bytes)
    def get_bytes(self) -> bytes


def registerNs(namespace: str, prefix: str)
def set_log_level(level=2)

def convert_exif_to_xmp(data: dict, encoding='utf-8') -> dict
def convert_iptc_to_xmp(data: dict, encoding='utf-8') -> dict
def convert_xmp_to_exif(data: dict, encoding='utf-8') -> dict
def convert_xmp_to_iptc(data: dict, encoding='utf-8') -> dict

__version__ = '2.15.3'
__exiv2_version__ = '0.28.3'
```

## class Image

- 类 `Image` 用于根据文件路径打开图片。例如：
    ```py
    >>> import pyexiv2
    >>> img = pyexiv2.Image(r'.\pyexiv2\tests\1.jpg')
    >>> data = img.read_exif()
    >>> img.close()
    ```
- pyexiv2 支持包含 Unicode 字符的图片路径、元数据。大部分函数都有一个默认参数：`encoding='utf-8'`。
  - 如果你因为图片路径、元数据包含非 ASCII 码字符而遇到错误，请尝试更换编码。例如：
    ```python
    img = pyexiv2.Image(path, encoding='utf-8')
    img = pyexiv2.Image(path, encoding='GBK')
    img = pyexiv2.Image(path, encoding='ISO-8859-1')
    ```
  - 另一个例子：中国地区的 Windows 电脑通常用 GBK 编码文件路径，因此它们不能被 utf-8 解码。
  - 另一个方案：如果你不想指定每个图片文件名的 encoding ，你可以用 Python 的 `open()` 函数打开图片文件，然后用 [pyexiv2.ImageData](https://github.com/LeoHsiao1/pyexiv2/blob/master/docs/Tutorial-cn.md#class-imagedata) 解析图片。

### close()

- 当你处理完图片之后，请记得调用 `img.close()` ，以释放用于存储图片数据的内存。
  - 不调用该方法会导致内存泄漏，但不会锁定文件描述符。
- 通过 `with` 关键字打开图片时，它会自动关闭图片。例如：
    ```py
    with pyexiv2.Image(r'.\pyexiv2\tests\1.jpg') as img:
        data = img.read_exif()
    ```

### read_xx()

- 读取元数据的示例:
    ```py
    >>> img.read_exif()
    {'Exif.Image.DateTime': '2019:06:23 19:45:17', 'Exif.Image.Artist': 'TEST', 'Exif.Image.Rating': '4', ...}
    >>> img.read_iptc()
    {'Iptc.Envelope.CharacterSet': '\x1b%G', 'Iptc.Application2.ObjectName': 'TEST', 'Iptc.Application2.Keywords': 'TEST', ...}
    >>> img.read_xmp()
    {'Xmp.dc.format': 'image/jpeg', 'Xmp.dc.rights': 'lang="x-default" TEST', 'Xmp.dc.subject': 'TEST', ...}
    >>> img.close()
    ```
- 上例只读取元数据的 `tag` 和 `value` 。你可以调用 `img.read_xx_detail()` 获取更多信息，包括 `typeName`、`tagDesc`、`tagLabel` 。
- 读取元数据的速度与元数据的数量成反比，不管图片的大小如何。
- 调用 `img.read_*()` 是安全的。这些方法永远不会影响图片文件（md5不变）。
- 读取 XMP 元数据时，空白字符 `\v` 和 `\f` 会被替换为空格 ` ` 。

### modify_xx()

- 修改元数据的示例:
    ```py
    >>> # 准备要修改的 XMP 数据
    >>> dict1 = {'Xmp.xmp.CreateDate': '2019-06-23T19:45:17.834',   # 给一个标签赋值。这将覆盖该标签的原始值，如果不存在该标签则添加它
    ...          'Xmp.xmp.Rating': None}                            # 赋值 None 会删除该标签
    >>> img.modify_xmp(dict1)
    >>> dict2 = img.read_xmp()       # 检查结果
    >>> dict2['Xmp.xmp.CreateDate']
    '2019-06-23T19:45:17.834'        # 这个标签被修改了
    >>> dict2['Xmp.xmp.Rating']
    KeyError: 'Xmp.xmp.Rating'       # 这个标签被删除了
    >>> img.close()
    ```
    - `img.modify_exif()` 和 `img.modify_iptc()` 的用法同理。
- 修改元数据的速度与图片的大小成反比。
- 修改非标准的标签可能引发异常。例如：
    ```py
    >>> img.modify_exif({'Exif.Image.mytag1': 'Hello'})
    RuntimeError: Invalid tag name or ifdId `mytag1', ifdId 1
    ```
    对于 XMP ，Exiv2 支持写入非标准的标签：
    ```py
    >>> img.modify_xmp({'Xmp.dc.mytag1': 'Hello'})
    >>> img.read_xmp()['Xmp.dc.mytag1']
    'Hello'
    ```
    对于 XMP ，Exiv2 会自动注册标准的命名空间、图片中已有的命名空间。你也可以主动注册命名空间：
    ```py
    >>> img.modify_xmp({'Xmp.test.mytag1': 'Hello'})
    RuntimeError: No namespace info available for XMP prefix `test'
    >>> pyexiv2.registerNs('a namespace for test', 'Ns1')
    >>> img.modify_xmp({'Xmp.Ns1.mytag1': 'Hello'})
    >>> img.read_xmp()['Xmp.Ns1.mytag1']
    'Hello'
    ```

- 某些特殊的标签不能被 pyexiv2 修改。例如：
    ```py
    >>> img.modify_exif({'Exif.Photo.MakerNote': 'Hello'})
    >>> img.read_exif()['Exif.Photo.MakerNote']
    ''
    ```

### clear_xx()

- 调用 `img.clear_exif()` 将删除图片的所有 EXIF 元数据。一旦清除元数据，pyexiv2 可能无法完全恢复它。因为某些特殊的标签不能被 pyexiv2 修改。
- `img.clear_iptc()` 和 `img.clear_xmp()` 的用法同理。

### comment

- `img.read_comment()`、`img.modify_comment()`、`img.clear_comment()` 用于访问图片里的 JPEG COM (COMMENT) 段，不属于 EXIF、IPTC、XMP 元数据。
  - [相关 Issue](https://github.com/Exiv2/exiv2/issues/1445)
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

### icc

- `img.read_icc()`、`img.modify_icc()`、`img.clear_icc()` 用于访问图片里的 [ICC profile](https://en.wikipedia.org/wiki/ICC_profile) 。

### thumbnail

- EXIF 标准允许在 JPEG 图片中嵌入缩略图，通常存储在 APP1 标签（FFE1）中。
- Exiv2 支持读写图像中的 EXIF 缩略图。但是只能插入 JPEG 缩略图（不能插入TIFF）。

### copy_xx()

- 以下代码用于从一个图片拷贝元数据到另一个图片：
  ```py
  with pyexiv2.Image(r'.\pyexiv2\tests\1.jpg') as img1:
      with pyexiv2.Image(r'.\pyexiv2\tests\2.jpg') as img2:
          img2.modify_exif(img1.read_exif())
          img2.modify_iptc(img1.read_iptc())
          img2.modify_xmp(img1.read_xmp())
  ```
  但更推荐以下代码：
  ```py
  with pyexiv2.Image(r'.\pyexiv2\tests\1.jpg') as img1:
      with pyexiv2.Image(r'.\pyexiv2\tests\2.jpg') as img2:
          # 如果不想保留第二张图像中已有的元数据，可以提前清除第二张图像
          # img2.clear_exif()
          # img2.clear_iptc()
          # img2.clear_xmp()
          img1.copy_to_another_image(img2, exif=True, iptc=True, xmp=True, comment=False, icc=False, thumbnail=False)
  ```
  理由如下：
  - 它的效率更高，因为不需要多次执行 modify_xx() 。
  - 一张图片的元数据可能是错误的格式，无法被 pyexiv2 解析，但仍然可以复制到另一张图片上。

## class ImageData

- 类 `ImageData` 继承于类 `Image`, 用于从字节数据中打开图片。
- 读取元数据的示例：
    ```py
    with open(r'.\pyexiv2\tests\1.jpg', 'rb') as f:
        with pyexiv2.ImageData(f.read()) as img:
            data = img.read_exif()
    ```
- 修改元数据的示例：
    ```py
    with open(r'.\pyexiv2\tests\1.jpg', 'rb+') as f:
        with pyexiv2.ImageData(f.read()) as img:
            changes = {'Iptc.Application2.ObjectName': 'test'}
            img.modify_iptc(changes)
            # 清空原文件
            f.seek(0)
            f.truncate()
            # 获取图片的字节数据并保存到文件中
            f.write(img.get_bytes())
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
- XMP 的 LangAlt 类型的标签有多种语言的值，它们会被转换成一个字典。例如：
    ```py
    >>> img.read_xmp()['Xmp.dc.title']
    {'lang="x-default"': 'test-中文-', 'lang="de-DE"': 'Hallo, Welt'}
    ```

## 日志

- Exiv2 有 5 种处理日志的级别：
    - 0 : debug
    - 1 : info
    - 2 : warn
    - 3 : error
    - 4 : mute

- `error` 日志会被转换成异常并抛出，其它日志则会被打印到 stdout 。
- 默认的日志级别是 `warn` ，因此更低级别的日志不会被报告。
- 调用函数 `pyexiv2.set_log_level()` 可以设置处理日志的级别。例如：
    ```py
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'}) # 此时有错误日志
    RuntimeError: XMP Toolkit error 102: Indexing applied to non-array
    Failed to encode XMP metadata.

    >>> pyexiv2.set_log_level(4)
    >>> img.modify_xmp({'Xmp.xmpMM.History': 'type="Seq"'}) # 此时没有错误日志
    ```

## convert

- Exiv2 支持将某些 EXIF 或 IPTC 标签，转换成 XMP 标签，也支持反向转换。参考：<https://github.com/Exiv2/exiv2/blob/v0.28.3/src/convert.cpp#L313>
- 示例：
    ```py
    >>> pyexiv2.convert_exif_to_xmp({'Exif.Image.Artist': 'test-中文-', 'Exif.Image.Rating': '4'})
    {'Xmp.dc.creator': ['test-中文-'], 'Xmp.xmp.Rating': '4'}
    ```

