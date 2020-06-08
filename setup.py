# -*- coding: utf-8 -*-
import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='pyexiv2',
    version='2.3.0',
    author='LeoHsiao',
    author_email='leohsiao@foxmail.com',
    description='Read/Write metadata of digital image, including EXIF, IPTC, XMP.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/LeoHsiao1/pyexiv2',
    # install_requires=["pybind11==2.4.3"],
    packages=setuptools.find_packages(),
    package_data={'': ['*.py', '*.md', '*.cpp', '*.so', '*.dll', '*.pyd', '*.jpg']},
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)


# upload to pypi.org:
#   python -m pip install setuptools wheel twine
#   git clean -d -fx
#   python setup.py sdist bdist_wheel
#   python -m twine upload dist/*
