# -*- coding: utf-8 -*-
import setuptools


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    name='pyexiv2',
    version='2.4.0',
    author='LeoHsiao',
    author_email='leohsiao@foxmail.com',
    description='Read/Write metadata of digital image, including EXIF, IPTC, XMP.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3',
    url='https://github.com/LeoHsiao1/pyexiv2',
    packages=setuptools.find_packages(),
    # packages=['pyexiv2', 'docs'],
    package_data={'': ['*']},
    python_requires='>=3.5',
    # install_requires=["pybind11"],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
