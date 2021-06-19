# lib

## File lists

```sh
.
├── py3*-darwin     # the build results of exiv2api.cpp on Darwin
├── py3*-linux      # the build results of exiv2api.cpp on Linux
├── py3*-win        # the build results of exiv2api.cpp on Windows
├── __init__.py
├── exiv2api.cpp    # Expose the API of exiv2 to Python
├── exiv2.dll       # Copied from the Exiv2 library for Windows
├── libexiv2.dylib  # Copied from the Exiv2 library for Darwin
├── libexiv2.so     # Copied from the Exiv2 library for Linux
└── README.md
```
- The distribution of pyexiv2 includes precompiled files, which can also be compiled by users.
- The principle of the pyexiv2 library:
  1. Write exiv2api.cpp to call the C++ API of the exiv2 library.
  2. Use Pybind11 to compile exiv2api.cpp into a Python module.
  3. Import the exiv2api module in the Python interpreter and call its API.
- The build results of exiv2api.cpp is not compatible with different platforms, or even with different minor versions of the Python interpreter.
- If the build results provided here do not apply to your platform, please compile it yourself. Then modify the code in `./__init__.py` so that it can successfully execute `import exiv2api`.
- Currently using version 0.27.4 of exiv2.

## Compile steps on Linux

1. Download the release version of Exiv2, unpack it.
    - Linux64 : <https://www.exiv2.org/archive.html>
    - For example:
        ```sh
        cd /root/
        curl -O https://www.exiv2.org/builds/exiv2-0.27.4-Linux64.tar.gz
        tar -zxvf exiv2-0.27.4-Linux64.tar.gz
        ```

2. Prepare the environment:
    ```sh
    EXIV2_DIR=/root/exiv2-0.27.4-Linux64   # According to your download location
    LIB_DIR=/root/pyexiv2/pyexiv2/lib/
    cp $EXIV2_DIR/lib/libexiv2.so.0.27.4  $EXIV2_DIR/lib/libexiv2.so
    cp $EXIV2_DIR/lib/libexiv2.so.0.27.4  $LIB_DIR/libexiv2.so
    ```

3. Set up the python interpreter. For example:
    ```sh
    py_version=8
    # docker run -it --rm --name python3.$py_version -e "py_version=$py_version" -e "EXIV2_DIR=$EXIV2_DIR" -e "LIB_DIR=$LIB_DIR" -v /root:/root python:3.$py_version-buster sh
    python3.$py_version -m pip install pybind11
    ```

4. Compile:
    ```sh
    cd $LIB_DIR
    mkdir -p py3${py_version}-linux
    g++ exiv2api.cpp -o py3${py_version}-linux/exiv2api.so \
        -O3 -Wall -std=c++11 -shared -fPIC \
        `python3.$py_version -m pybind11 --includes` \
        -I $EXIV2_DIR/include \
        -L $EXIV2_DIR/lib \
        -l exiv2
    ```

## Compile steps on Darwin

1. Download the release version of Exiv2, unpack it.
    - Darwin : <https://www.exiv2.org/archive.html>
    - For example:
        ```sh
        cd /Users/leo/Documents/
        curl -O https://www.exiv2.org/builds/exiv2-0.27.4-Darwin.tar.gz
        tar -zxvf exiv2-0.27.4-Darwin.tar.gz
        ```

2. Prepare the environment:
    ```sh
    EXIV2_DIR=/Users/leo/Documents/exiv2-0.27.4-Darwin
    LIB_DIR=/Users/leo/Documents/pyexiv2/pyexiv2/lib/
    cp ${EXIV2_DIR}/lib/libexiv2.0.27.4.dylib ${LIB_DIR}/libexiv2.dylib
    ```

3. Set up the python interpreter. For example:
    ```sh
    py_version=8
    python3.$py_version -m pip install pybind11
    ```

4. Compile:
    ```sh
    cd $LIB_DIR
    g++ exiv2api.cpp -o py3${py_version}-darwin/exiv2api.so \
        -O3 -Wall -std=c++11 -shared -fPIC \
        `python3.$py_version -m pybind11 --includes` \
        -I $EXIV2_DIR/include \
        -L $EXIV2_DIR/lib \
        -l exiv2 \
        -undefined dynamic_lookup
    ```

## Compile steps on Windows

1. Download the release version of Exiv2 project.
    - msvc64 : <https://www.exiv2.org/archive.html>
    - For example:
        ```sh
        curl -O https://www.exiv2.org/releases/exiv2-0.27.4-2019msvc64.zip
        ```

2. Install `Visual Studio 2019` (must use the same version of Visual Studio as the Exiv2 build) , and set the environment variables it needs.

3. Prepare the environment:
    ```batch
    "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
    set EXIV2_DIR=C:\Users\Leo\Downloads\exiv2-0.27.4-2019msvc64
    cd pyexiv2\lib
    copy %EXIV2_DIR%\bin\exiv2.dll .
    ```

4. Compile:
    ```batch
    set py_version=8
    set py_home=%APPDATA%\..\Local\Programs\Python\Python3%py_version%
    cl /MD /LD exiv2api.cpp /EHsc -I %EXIV2_DIR%\include -I %py_home%\include -I %py_home%\Lib\site-packages\pybind11\include /link %EXIV2_DIR%\lib\exiv2.lib %py_home%\libs\python3%py_version%.lib /OUT:py3%py_version%-win\exiv2api.pyd
    del exiv2api.exp exiv2api.obj exiv2api.lib
    ```
    - Modify the path here according to your installation location.
