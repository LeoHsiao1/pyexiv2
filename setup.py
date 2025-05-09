# -*- coding: utf-8 -*-
import setuptools


with open('README.md', encoding='utf-8') as f:
    readme_md = f.read()


setuptools.setup(
    name='pyexiv2',
    version='2.15.4',    # need to set the variable in 'pyexiv2/__init__.py'
    author='LeoHsiao',
    author_email='leohsiao@foxmail.com',
    description='Read and write image metadata, including EXIF, IPTC, XMP, ICC Profile.',
    long_description=readme_md,
    long_description_content_type='text/markdown',
    license='GPLv3',
    url='https://github.com/LeoHsiao1/pyexiv2',
    packages=setuptools.find_packages(),
    # packages=['pyexiv2', 'docs'],
    package_data={'': ['*', '*/*']},
    python_requires='>=3.8',
    # install_requires=["pybind11"],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
    ],
)