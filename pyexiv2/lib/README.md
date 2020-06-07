# lib

## File lists

```
.
├── linux64-py3*    # the build results on Linux(64bit)
├── win64-py3*      # the build results on Windows(64bit)
├── __init__.py
├── exiv2api.cpp    # Expose the API of exiv2 to Python
├── exiv2.dll       # Copied from the Exiv2 release
├── libexiv2.so     # Copied from the Exiv2 release
└── README.md
```
- The current release version of Exiv2 is `0.27.2`.
- You need to install pybind11 to compile exiv2api.cpp : `python3 -m pip install pybind11`
- When using pyexiv2, you must use the same Python interpreter as the compile-time version.
- On the development branch, it is not necessary to compile all versions of exiv2api.cpp and save them to the git repository.

## Compile steps on Linux

1. Download the release version of Exiv2, unpack it.
    - Linux64 : <https://www.exiv2.org/builds/>
    - For example:
        ```sh
        cd /root/pyexiv2/
        curl -O https://www.exiv2.org/builds/exiv2-0.27.2-Linux64.tar.gz
        tar -zxvf exiv2-0.27.2-Linux64.tar.gz
        ```

2. Prepare the environment:
    ```sh
    EXIV2_DIR=/root/pyexiv2/exiv2-0.27.2-Linux64   # According to your download location
    LIB_DIR=/root/pyexiv2/pyexiv2/lib/
    cp ${EXIV2_DIR}/lib/libexiv2.so.0.27.2 $LIB_DIR/libexiv2.so
    ```

3. Set up the python interpreter. For example:
    ```sh
    py_version=8
    docker run -it --rm --name python3.$py_version -e "py_version=$py_version" -e "EXIV2_DIR=$EXIV2_DIR" -e "LIB_DIR=$LIB_DIR" -v /root/pyexiv2:/root/pyexiv2 python:3.$py_version bash
    python3.$py_version -m pip install pybind11
    ```

4. Compile:
    ```sh
    cd $LIB_DIR
    g++ exiv2api.cpp -o linux64-py3${py_version}/exiv2api.so -O3 -Wall -std=c++11 -shared -fPIC `python3.$py_version -m pybind11 --includes` -I ${EXIV2_DIR}/include -L ${EXIV2_DIR}/lib -l exiv2
    ```

## Compile steps on Darwin

1. Download the release version of Exiv2, unpack it.
    - Darwin : <https://www.exiv2.org/builds/>
    - For example:
        ```sh
        cd /Users/leo/Documents/
        curl -O https://www.exiv2.org/builds/exiv2-0.27.2-Darwin.tar.gz
        tar -zxvf exiv2-0.27.2-Darwin.tar.gz
        ```

2. Prepare the environment:
    ```sh
    EXIV2_DIR=/Users/leo/Documents/exiv2-0.27.2-Darwin
    LIB_DIR=/Users/leo/Documents/pyexiv2/pyexiv2/lib/
    cp ${EXIV2_DIR}/lib/libexiv2.0.27.2.dylib ${LIB_DIR}/libexiv2.dylib
    ```

3. Set up the python interpreter. For example:
    ```sh
    py_version=8
    python3.$py_version -m pip install pybind11
    ```

4. Compile:
    ```sh
    cd $LIB_DIR
    g++ exiv2api.cpp -o darwin64-py3${py_version}/exiv2api.so -O3 -Wall -std=c++11 -shared -fPIC `python3.$py_version -m pybind11 --includes` -I ${EXIV2_DIR}/include -L ${EXIV2_DIR}/lib -l exiv2 -undefined dynamic_lookup
    ```

## Compile steps on Windows

1. Download the release version of Exiv2 project.
    - msvc64 : <https://www.exiv2.org/builds/>

2. Install `Visual Studio 2017` (must use the same version of Visual Studio as the Exiv2 build) , and set the environment variables it needs.

3. Prepare the environment:
    ```batch
    "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
    set EXIV2_DIR=C:\Users\Leo\Downloads\exiv2-0.27.2-2017msvc64
    cd pyexiv2\lib
    copy %EXIV2_DIR%\bin\exiv2.dll .
    ```

4. Compile:
    ```batch
    set py_version=8
    cl /MD /LD exiv2api.cpp /EHsc -I %EXIV2_DIR%\include -I C:\Users\Leo\AppData\Local\Programs\Python\Python3%py_version%\include /link %EXIV2_DIR%\lib\exiv2.lib C:\Users\Leo\AppData\Local\Programs\Python\Python3%py_version%\libs\python3%py_version%.lib /OUT:win64-py3%py_version%\exiv2api.pyd
    del exiv2api.exp exiv2api.obj exiv2api.lib
    ```
    Modify the path here according to your installation location.
