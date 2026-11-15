import os
import sys
import ctypes

# Recognize the Python interpreter
if sys.maxsize <= 2**32:
    raise RuntimeError('pyexiv2 can only run on 64-bit python3 interpreter.')

# Recognize the system
lib_dir     = os.path.dirname(__file__)
sys_name    = {'linux': 'Linux', 'darwin': 'Darwin', 'win32': 'Windows'}.get(sys.platform, sys.platform)
if sys_name == 'Linux':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.so'))
    
    from . import exiv2api
elif sys_name == 'Darwin':
    ctypes.CDLL(os.path.join(lib_dir, 'libexiv2.dylib'))
    from . import exiv2api
elif sys_name == 'Windows':
    ctypes.CDLL(os.path.join(lib_dir, 'exiv2.dll'))
    from . import exiv2api
else:
    raise RuntimeError('pyexiv2 can only run on Linux, Darwin or Windows system. But your system is {} .'.format(sys_name))
