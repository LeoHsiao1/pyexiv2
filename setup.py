# -*- coding: utf-8 -*-
import setuptools

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pyexiv2",
    version="1.3.0",
    author="LeoHsiao",
    author_email="leohsiao@foxmail.com",
    description="Read/Write metadata of digital image, including EXIF, IPTC, XMP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeoHsiao1/pyexiv2",
    packages=setuptools.find_packages(),
    package_data={"pyexiv2": ["lib/*", "tests/*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
)


# upload to pypi.org:
#   python setup.py sdist bdist_wheel
#   python -m twine upload dist/*
