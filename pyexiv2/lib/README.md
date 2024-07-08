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
- The build results of pyexiv2 is not compatible with different platforms, or even with different minor versions of the Python interpreter.
- You can execute `pip install pyexiv2` to install pyexiv2. It contains some compiled library files.
  - You can download the source code and compile it manually. Then modify the code in `./__init__.py` so that it can successfully execute `import exiv2api`.
  - You can also fork the GitHub project and use [GitHub Action](../../.github/workflows/build.yml) to build.

## Compile steps on Linux

1. Download [the release of Exiv2](https://www.exiv2.org/archive.html) :
    ```sh
    curl -O https://github.com/Exiv2/exiv2/releases/download/v0.28.3/exiv2-0.28.3-Linux64.tar.gz
    tar -zxvf exiv2-0.28.3-Linux64.tar.gz
    ```

2. Prepare environment variables according to your download path:
    ```sh
    EXIV2_DIR=??/exiv2-0.28.3-Linux64
    LIB_DIR=??/pyexiv2/lib/
    cp $EXIV2_DIR/lib/libexiv2.so.0.28.3  $EXIV2_DIR/lib/libexiv2.so
    cp $EXIV2_DIR/lib/libexiv2.so.0.28.3  $LIB_DIR/libexiv2.so
    ```

3. Prepare the python interpreter:
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
    You will get a library file:
    ```sh
    ls -lh py3.${py_version}-linux/exiv2api.so
    ```

## Compile steps on Darwin

1. Download [the release of Exiv2](https://www.exiv2.org/archive.html) :
    ```sh
    curl -O https://github.com/Exiv2/exiv2/releases/download/v0.28.3/exiv2-0.28.3-Darwin.tar.gz
    tar -zxvf exiv2-0.28.3-Darwin.tar.gz
    ```

2. Prepare environment variables according to your download path:
    ```sh
    EXIV2_DIR=??/exiv2-0.28.3-Darwin
    LIB_DIR=??/pyexiv2/lib
    cp ${EXIV2_DIR}/lib/libexiv2.0.28.3.dylib ${LIB_DIR}/libexiv2.dylib
    ```

3. Prepare the python interpreter:
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
    You will get a library file:
    ```sh
    ls -lh py3.${py_version}-darwin/exiv2api.so
    ```

## Compile steps on Windows

1. Download [the release of Exiv2](https://www.exiv2.org/archive.html) :
    ```sh
    curl -O https://github.com/Exiv2/exiv2/releases/download/v0.28.3/exiv2-0.28.3-2019msvc64.zip
    python -m zipfile -e exiv2-0.28.3-2019msvc64.zip .
    ```

2. Install `Visual Studio 2019` (must use the same version of Visual Studio as the Exiv2 build) , and set the environment variables it needs.

3. Prepare environment variables according to your download path:
    ```batch
    "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
    set  EXIV2_DIR=??\exiv2-0.28.3-2019msvc64
    set  LIB_DIR=??\pyexiv2\lib
    copy %EXIV2_DIR%\bin\exiv2.dll  %LIB_DIR%
    ```

4. Prepare the python interpreter:
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
    You will get a library file:
    ```batch
    dir py3.%py_version%-win\exiv2api.pyd
    ```
