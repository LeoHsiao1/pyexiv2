import os
import sys
import ctypes
import platform


if platform.architecture()[0] != '64bit':
    raise RuntimeError('pyexiv2 can only run on 64-bit python3 interpreter.')

# Check the Python interpreter
py_version = platform.python_version()[:3]
expected_py_version = ['3.5', '3.6', '3.7', '3.8', '3.9']
if py_version not in expected_py_version:
    raise RuntimeError('pyexiv2 only supports these Python versions: {} . But your version is {} .'.format(expected_py_version, py_version))

lib_dir = os.path.dirname(__file__)

# Recognize the system
sys_name = platform.system() or 'Unknown'
if sys_name == 'Linux':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so')) # import the exiv2 library at first, otherwise the Python interpreter can not find it.
    sys.path.append(os.path.join(lib_dir, 'py{}-linux'.format(py_version.replace('.', ''))))
    import exiv2api
elif sys_name == 'Darwin':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.dylib'))
    sys.path.append(os.path.join(lib_dir, 'py{}-darwin'.format(py_version.replace('.', ''))))
    import exiv2api
elif sys_name == 'Windows':
    ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
    sys.path.append(os.path.join(lib_dir, 'py{}-win'.format(py_version.replace('.', ''))))
    import exiv2api
else:
    raise RuntimeError('pyexiv2 can only run on Linux, Darwin or Windows system. But your system is {} .'.format(sys_name))
