# lib

## File lists

```sh
.
├── py3.*-darwin    # the build results of exiv2api.cpp on Darwin
├── py3.*-linux     # the build results of exiv2api.cpp on Linux
├── py3.*-win       # the build results of exiv2api.cpp on Windows
├── __init__.py
├── exiv2api.cpp    # Expose the API of exiv2 to Python
├── exiv2.dll       # Copied from the Exiv2 library for Windows
├── libexiv2.dylib  # Copied from the Exiv2 library for Darwin
├── libexiv2.so     # Copied from the Exiv2 library for Linux
└── README.md
```
- The principle of the pyexiv2 library:
  1. Write exiv2api.cpp to call the C++ API of the exiv2 library.
  2. Use Pybind11 to compile exiv2api.cpp into a Python module.
  3. Import the exiv2api module in the Python interpreter and call its API.
- The version of Exiv2 in use is 0.27.5 .
- The distribution of pyexiv2 includes compiled files, so users can use it directly.
  - You can compile pyexiv2 according to this document.
  - You can also fork the project and use the the [build workflow](../../.github/workflows/build.yml) on GitHub.
- The build results of pyexiv2 is not compatible with different platforms, or even with different minor versions of the Python interpreter.
  - If the build results provided here are not compatible with your platform, you can compile it yourself. Then modify the code in `./__init__.py` so that it can successfully execute `import exiv2api`.

## Compile steps on Linux

1. Download the release version of Exiv2, unpack it.
    - Linux64 : <https://www.exiv2.org/archive.html>
    - For example:
        ```sh
        cd /root/
        curl -O https://github.com/Exiv2/exiv2/releases/download/v0.27.5/exiv2-0.27.5-Linux64.tar.gz
        tar -zxvf exiv2-0.27.5-Linux64.tar.gz
        ```

2. Prepare environment variables according to your path:
    ```sh
    EXIV2_DIR=/mnt/c/Users/Leo/Downloads/exiv2-0.27.5-Linux64
    LIB_DIR=$PWD/pyexiv2/lib/
    cp $EXIV2_DIR/lib/libexiv2.so.0.27.5  $EXIV2_DIR/lib/libexiv2.so
    cp $EXIV2_DIR/lib/libexiv2.so.0.27.5  $LIB_DIR/libexiv2.so
    ```

3. Set up the python interpreter:
    ```sh
    py_version=8
    python3.$py_version -m pip install pybind11
    ```

4. Compile:
    ```sh
    cd $LIB_DIR
    mkdir -p py3.${py_version}-linux
    g++ exiv2api.cpp -o py3.${py_version}-linux/exiv2api.so \
        -std=c++11 -O3 -Wall -shared -fPIC \
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
        curl -O https://github.com/Exiv2/exiv2/releases/download/v0.27.5/exiv2-0.27.5-Darwin.tar.gz
        tar -zxvf exiv2-0.27.5-Darwin.tar.gz
        ```

2. Prepare environment variables according to your path:
    ```sh
    EXIV2_DIR=/Users/leo/Documents/exiv2-0.27.5-Darwin
    LIB_DIR=$PWD/pyexiv2/lib
    cp ${EXIV2_DIR}/lib/libexiv2.0.27.5.dylib ${LIB_DIR}/libexiv2.dylib
    ```

3. Set up the python interpreter:
    ```sh
    py_version=8
    python3.$py_version -m pip install pybind11
    ```

4. Compile:
    ```sh
    cd $LIB_DIR
    g++ exiv2api.cpp -o py3.${py_version}-darwin/exiv2api.so \
        -std=c++11 -O3 -Wall -shared -fPIC \
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
        curl -O https://github.com/Exiv2/exiv2/releases/download/v0.27.5/exiv2-0.27.5-2019msvc64.zip
        ```

2. Install `Visual Studio 2019` (must use the same version of Visual Studio as the Exiv2 build) , and set the environment variables it needs.

3. Prepare environment variables according to your path:
    ```batch
    "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
    set  EXIV2_DIR=C:\Users\Leo\Downloads\exiv2-0.27.5-2019msvc64
    set  LIB_DIR=%CD%\pyexiv2\lib
    copy %EXIV2_DIR%\bin\exiv2.dll  %LIB_DIR%
    ```

4. Set up the python interpreter:
    ```batch
    set  py_version=8
    set  PY_HOME=%APPDATA%\..\Local\Programs\Python\Python3%py_version%
    python3.$py_version -m pip install pybind11
    ```

5. Compile:
    ```batch
    cd  %LIB_DIR%
    cl /MD /LD exiv2api.cpp /EHsc -I %EXIV2_DIR%\include -I %PY_HOME%\include -I %PY_HOME%\Lib\site-packages\pybind11\include /link %EXIV2_DIR%\lib\exiv2.lib %PY_HOME%\libs\python3%py_version%.lib /OUT:py3.%py_version%-win\exiv2api.pyd
    del exiv2api.exp exiv2api.obj exiv2api.lib
    ```
