import os
import sys
import ctypes
import platform


# Check the Python interpreter
if platform.architecture()[0] != '64bit':
    raise RuntimeError('pyexiv2 can only run on 64-bit python3 interpreter.')
py_version = platform.python_version()[:3]
if py_version not in ['3.5', '3.6', '3.7', '3.8']:
    raise RuntimeError('pyexiv2 only supports these Python versions: 3.5, 3.6, 3.7, 3.8 , but your version is {} .'.format(py_version))

lib_dir = os.path.dirname(__file__)

# Recognize the system
sys_name = platform.system() or 'Unknown'
if sys_name == 'Linux':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so')) # import the library at first, otherwise the Python interpreter can not find it.
    sys.path.append(os.path.join(lib_dir, 'linux64-py{}'.format(py_version.replace('.', ''))))
    import exiv2api
elif sys_name == 'Windows':
    ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
    sys.path.append(os.path.join(lib_dir, 'win64-py{}'.format(py_version.replace('.', ''))))
    import exiv2api
else:
    raise RuntimeError('pyexiv2 can only run on Linux(64bit) or Windows(64bit), but your system is {} .'.format(sys_name))
