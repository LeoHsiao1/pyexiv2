# lib

## File lists

```
.
├── __init__.py
├── README.md
├── api.cpp             # Expose the API of exiv2 to Python. It needs to be compiled by pybind11.
├── linux64
│   ├── __init__.py
│   ├── api.so          # The result of compilation on Linux(64bit)
│   └── libexiv2.so     # Copied from Exiv2 project
└── win64
    ├── __init__.py
    ├── api.pyd         # The result of compilation on Windows(64bit)
    └── exiv2.dll       # Copied from Exiv2 project
```
- The current release version of Exiv2 is `0.27.2` .

## Compile steps on Linux

1. Download the release version of Exiv2, unpack it.
    - Linux64 : <https://www.exiv2.org/builds/>

2. install g++ .

3. Prepare the environment:
    ```sh
    cd ./linux64
    EXIV2_DIR=/mnt/c/Users/Leo/Downloads/exiv2-0.27.2-Linux64   # According to your download location
    mv ${EXIV2_DIR}/lib/libexiv2.so.0.27.2 ${EXIV2_DIR}/lib/libexiv2.so     # rename the library file
    cp ${EXIV2_DIR}/lib/libexiv2.so .
    ```

4. Compile:
    ```sh
    g++ ../api.cpp -o api.so -O3 -Wall -std=c++11 -shared -fPIC `python3 -m pybind11 --includes` -I ${EXIV2_DIR}/include -L ${EXIV2_DIR}/lib -l exiv2
    ```

## Compile steps on Windows

1. Download the release version of Exiv2 project.
    - msvc64 : <https://www.exiv2.org/builds/>

2. Install `Visual Studio 2017` (must use the same version of Visual Studio as the Exiv2 build) , and set the environment variables it needs.

3. Prepare the environment:
    ```
    "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
    cd .\win64
    set EXIV2_DIR=C:\Users\Leo\Downloads\exiv2-0.27.2-2017msvc64
    copy %EXIV2_DIR%\bin\exiv2.dll .
    ```

4. Compile:
    ```
    cl /MD /LD ..\api.cpp /EHsc -I %EXIV2_DIR%\include -I C:\Users\Leo\AppData\Local\Programs\Python\Python37\include /link %EXIV2_DIR%\lib\exiv2.lib C:\Users\Leo\AppData\Local\Programs\Python\Python37\libs\python37.lib /OUT:api.pyd
    del api.exp api.obj api.lib
    ```
    Modify the path here according to your installation location.
