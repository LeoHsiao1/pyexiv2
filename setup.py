import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="pyexiv2",
    version="1.0.0",
    author="LeoHsiao",
    author_email="leohsiao@foxmail.com",
    description="Read and modify metadata of digital image, including EXIF, IPTC, XMP.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeoHsiao1/pyexiv2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
)
