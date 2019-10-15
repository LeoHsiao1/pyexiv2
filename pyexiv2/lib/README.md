# About The Library

- `api.cpp` : wrote by the programmer.
- `api.so` , `api.dll` : compiled from api.cpp, will be called by Python program.
- `libexiv2.so` , `exiv2.dll` : copied from the release version of Exiv2 project.
  - The current version is Exiv2 0.27.2.

---

## compile steps of api.so on Linux

1. Download the release version of Exiv2 project.
    - Linux64 : <https://www.exiv2.org/builds/>

2. install `g++`

3. Copy `api.cpp` into the directory of Exiv2 project.
    - Modify its contents:

    ```C++
    #define API extern "C" // on Linux
    //#define API extern "C" __declspec(dllexport) // on Windows
    ```

4. Execute compile command, to generate dynamic library.

    ```cmd
    g++ -std=c++98 api.cpp -o api.so -shared -fPIC -I $PWD/include -L $PWD/lib -l Exiv2
    ```

5. Copy `lib/libexiv2.so` and `api.so` to the this folder `pyexiv2/lib/`.

---

## compile steps of api.dll on Windows

1. Download the release version of Exiv2 project.
    - msvc64 : <https://www.exiv2.org/builds/>

2. Install `Visual Studio 2017`(must use the same version of Visual Studio as the Exiv2 build), and set the environment variables it needs.

3. Copy `api.cpp` into the directory of Exiv2 project.
    - Modify its contents:

    ```C++
    //#define API extern "C" // on Linux
    #define API extern "C" __declspec(dllexport) // on Windows
    ```

4. Open the CMD window, set the environment variables of Exiv2 project.

    ```cmd
    cd <exiv2_dir>
    set PATH=%CD%\bin;%PATH%
    ```

5. Run `vcvars64.bat` to initialize the DOS environment, like this:

    ```cmd
    "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat"
    ```

6. Execute compile command, to generate dynamic library.

    ```cmd
    cl /MD /LD api.cpp /EHsc -I include /link lib/exiv2.lib
    ```

7. Copy `bin/exiv2.dll` and `api.dll` to the this folder `pyexiv2/lib/`.
