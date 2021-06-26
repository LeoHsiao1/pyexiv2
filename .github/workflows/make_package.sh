#!/bin/bash

######
# This script is used to make the distribution packages for pyexiv2.
# Execute this script with `bash .github/workflows/make_package.sh`.
# If you execute this script in WSL, you need to grant "Full control" to "Authenticated Users" in the Windows File settings for the folder.
######

set -e
echo WORK_DIR: `pwd`

WORK_DIR=`pwd`
LIB_DIR=`pwd`/pyexiv2/lib
TEST_DIR=`pwd`/pyexiv2/tests

if [ ! -f setup.py ]
then
    echo '[ERROR] The current directory is not the project root directory.'
    exit 1
fi

reset_workdir(){
    cd $WORK_DIR
    git reset --hard
    git clean -dfx build pyexiv2 pyexiv2.egg-info
}

# Install dependencies
python3 -m pip install setuptools wheel twine 

# Clear dist directory
rm -rf dist/*

## Make a source package without compiled files
# reset_workdir
# cd $LIB_DIR
# rm -rf libexiv2.so  libexiv2.dylib  exiv2.dll  py3*
# cd $WORK_DIR
# python3 setup.py sdist

## Make a wheel package that contains all compiled files
# reset_workdir
# rm -rf $TEST_DIR
# python3 setup.py bdist_wheel --python-tag cp3
# cd dist
# whl_name=`ls *cp3-none-any.whl`
# mv $whl_name ${whl_name/-none-any/}

make_wheels(){
    for version in {5..9}
    do
        reset_workdir
        rm -rf $TEST_DIR
        cd $LIB_DIR
        rm -rf $rm_files
        find . -maxdepth 1 -type d -name 'py3*' | grep -v py3${version}-${plat_type} | xargs rm -rf
        cd $WORK_DIR
        python3 setup.py bdist_wheel --python-tag cp3${version}  --plat-name ${plat_name}
    done
}

## Make wheel packages for any platform
# plat_type=
# plat_name=any
# rm_files=''
# make_wheels

## Make wheel packages for Linux platform
plat_type=linux
plat_name=manylinux2014_x86_64
rm_files='libexiv2.dylib  exiv2.dll'
make_wheels

## Make wheel packages for MacOS platform
plat_type=darwin
plat_name=macosx_10_14_x86_64.macosx_11_0_x86_64
rm_files='libexiv2.so  exiv2.dll'
make_wheels

## Make wheel packages for Windows platform
plat_type=win
plat_name=win_amd64
rm_files='libexiv2.so  libexiv2.dylib'
make_wheels

reset_workdir

# upload to pypi.org
twine upload dist/*
