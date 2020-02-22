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

2. Download the python interpreter, for example:
    ```sh
    docker run -d --name python3.5 -v /root/pyexiv2:/root/pyexiv2 python:3.5 tail -f /dev/null
    docker exec -it python3.5 bash
    ```

3. install g++ .

4. Prepare the environment:
    ```sh
    cd pyexiv2/lib/
    EXIV2_DIR=/mnt/c/Users/Leo/Downloads/exiv2-0.27.2-Linux64   # According to your download location
    mv ${EXIV2_DIR}/lib/libexiv2.so.0.27.2 ${EXIV2_DIR}/lib/libexiv2.so     # rename the library file
    cp ${EXIV2_DIR}/lib/libexiv2.so .
    ```

5. Compile:
    ```sh
    g++ exiv2api.cpp -o linux64-py35/exiv2api.so -O3 -Wall -std=c++11 -shared -fPIC `python3.5 -m pybind11 --includes` -I ${EXIV2_DIR}/include -L ${EXIV2_DIR}/lib -l exiv2
    ```

## Compile steps on Windows

1. Download the release version of Exiv2 project.
    - msvc64 : <https://www.exiv2.org/builds/>

2. Install `Visual Studio 2017` (must use the same version of Visual Studio as the Exiv2 build) , and set the environment variables it needs.

3. Prepare the environment:
    ```
    "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
    cd pyexiv2\lib
    set EXIV2_DIR=C:\Users\Leo\Downloads\exiv2-0.27.2-2017msvc64
    copy %EXIV2_DIR%\bin\exiv2.dll .
    ```

4. Compile:
    ```
    set py_version=35
    cl /MD /LD exiv2api.cpp /EHsc -I %EXIV2_DIR%\include -I C:\Users\Leo\AppData\Local\Programs\Python\Python%py_version%\include /link %EXIV2_DIR%\lib\exiv2.lib C:\Users\Leo\AppData\Local\Programs\Python\Python%py_version%\libs\python%py_version%.lib /OUT:win64-py%py_version%\exiv2api.pyd
    del exiv2api.exp exiv2api.obj exiv2api.lib
    ```
    Modify the path here according to your installation location.
