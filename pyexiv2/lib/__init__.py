import os
import sys
import ctypes
import platform

# Recognize the Python interpreter
if platform.architecture()[0] != '64bit':
    raise RuntimeError('pyexiv2 can only run on 64-bit python3 interpreter.')

# Recognize the system
lib_dir     = os.path.dirname(__file__)
sys_name    = platform.system() or 'Unknown'
if sys_name == 'Linux':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so'))
    sys.path.append(os.path.join(lib_dir))
    import exiv2api
elif sys_name == 'Darwin':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.dylib'))
    sys.path.append(os.path.join(lib_dir))
    import exiv2api
elif sys_name == 'Windows':
    ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
    sys.path.append(os.path.join(lib_dir))
    import exiv2api
else:
    raise RuntimeError('pyexiv2 can only run on Linux, Darwin or Windows system. But your system is {} .'.format(sys_name))
