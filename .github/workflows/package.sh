#!/bin/bash

######
# It is recommended that this script be executed using bash instead of sh .
# If you execute this script in WSL, you need to grant "Full control" to "Authenticated Users" in the Windows File settings for the folder.
######

WORK_DIR=`pwd`
echo WORK_DIR: $WORK_DIR

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
# python3 -m pip install setuptools wheel twine

# Clear dist directory
rm -rf dist/*

# Make a source package
reset_workdir
rm -rf pyexiv2/lib/py3*     # Delete all compiled files
python3 setup.py sdist

# Make a wheel package
reset_workdir
rm -rf pyexiv2/tests/       # Delete tests directory
python3 setup.py bdist_wheel --python-tag cp3
cd dist
whl_name=`ls *cp3-none-any.whl`
mv $whl_name ${whl_name/-none-any/}


# Make a wheel package that contains only compiled files for a single platform
# reset_workdir
# cd pyexiv2/lib/
# rm -rf  *.dylib  *.dll  py*-darwin  py*-win
# ls py* | grep -v 'py35-linux'
# find . -maxdepth 1 -type d -name 'py*' | grep -v py35-linux | xargs rm -rf
# cd $WORK_DIR
# python3 setup.py bdist_wheel --python-tag cp35  --plat-name linux_x86_64



reset_workdir

# upload to pypi.org
twine upload dist/*

