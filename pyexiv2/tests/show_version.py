import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import platform
print(platform.uname())

import pyexiv2
print('__path__={}'.format(pyexiv2.__path__))
print('__version__={}'.format(pyexiv2.__version__))
print('__exiv2_version__={}'.format(pyexiv2.__exiv2_version__))
