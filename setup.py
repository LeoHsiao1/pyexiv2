# -*- coding: utf-8 -*-
import setuptools

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='pyexiv2',
    version='2.3.2',
    author='LeoHsiao',
    author_email='leohsiao@foxmail.com',
    description='Read/Write metadata of digital image, including EXIF, IPTC, XMP.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPLv3',
    url='https://github.com/LeoHsiao1/pyexiv2',
    # packages=setuptools.find_packages(),
    packages=['pyexiv2', 'pyexiv2/lib', 'docs'],
    package_data={'': ['*.py', '*.md', '*.cpp',
                       '*.so', '*.dylib', '*.dll', '*.pyd', '*.jpg']},
    python_requires='>=3.5',
    # install_requires=["pybind11==2.4.3"],
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


# upload to pypi.org:
#   python -m pip install setuptools wheel twine
#   git clean -d -fx
#   python setup.py sdist bdist_wheel   # then rename pyexiv2-x.x.x-py3-none-any.whl to pyexiv2-x.x.x.whl
#   twine upload dist/*
