#!/bin/bash

######
# This script is used to make the distribution packages for pyexiv2.
# Execute this script with `bash .github/workflows/make_package.sh`.
# If you execute this script in WSL, you need to grant "Full control" to "Authenticated Users" in the Windows File settings for the folder.
######

set -eu
WORK_DIR=`git rev-parse --show-toplevel`
echo WORK_DIR: $WORK_DIR

if [ ! -f setup.py ]
then
    echo '[ERROR] WORK_DIR is valid.'
    exit 1
fi

LIB_DIR=$WORK_DIR/pyexiv2/lib
TEST_DIR=$WORK_DIR/pyexiv2/tests
DIST_DIR=$WORK_DIR/dist
EXIV2_LIB_FILES='libexiv2.so  libexiv2.dylib  exiv2.dll'

reset_workdir(){
    cd $WORK_DIR
    git reset --hard
    git clean -dfx build pyexiv2 pyexiv2.egg-info
}

# Install dependencies
python3 -m pip install setuptools wheel twine 

# Clear dist directory
rm -rf $DIST_DIR

## Make a source package without compiled files
# reset_workdir
# cd $LIB_DIR
# rm -rf  $EXIV2_LIB_FILES  py3*
# cd $WORK_DIR
# python3 setup.py sdist

## Make a wheel package that contains all compiled files
# reset_workdir
# rm -rf $TEST_DIR
# python3 setup.py bdist_wheel --python-tag cp3
# cd $DIST_DIR
# whl_name=`ls *cp3-none-any.whl`
# mv $whl_name ${whl_name/-none-any/}

make_wheels(){
    for version in {5..9}
    do
        reset_workdir
        rm -rf $TEST_DIR
        cd $LIB_DIR
        ls $EXIV2_LIB_FILES | grep -v $EXIV2_LIB_FILE | xargs rm -f
        find . -maxdepth 1 -type d -name 'py3*' | grep -v py3${version}-${plat_type} | xargs rm -rf
        cd $WORK_DIR
        python3 setup.py bdist_wheel --python-tag cp3${version}  --plat-name ${plat_name}
    done
}

# Make wheel packages for Linux platform
plat_type=linux
plat_name=manylinux2014_x86_64
EXIV2_LIB_FILE='libexiv2.so'
make_wheels

# Make wheel packages for MacOS platform
plat_type=darwin
plat_name=macosx_10_14_x86_64
EXIV2_LIB_FILE='libexiv2.dylib'
make_wheels
# Add plat_name for MacOS platform
cd $DIST_DIR
for f in `ls | grep ${plat_name}`
do
    mv  $f  ${f/.whl/.macosx_11_0_x86_64.whl}
done

# Make wheel packages for Windows platform
plat_type=win
plat_name=win_amd64
EXIV2_LIB_FILE='exiv2.dll'
make_wheels

reset_workdir

# upload to pypi.org
twine upload $DIST_DIR/*
