# About These Libraries

- `api.cpp` : write by the programmer.
- `libexiv2.so` , `exiv2.dll` : copied from the release version of exiv2 project.
- `api.so` , `api.dll` : compiled from api.cpp, will be called by Python program.

---

## edit api.cpp

TODO:

- Remove some duplicate code
- Do not use global variables, to become thread-safe
- Maybe use some C++ classes, callback functions

---

## compile steps of api.so on Linux

1. Download the release version of exiv2 project.
    - Linux64 : <https://www.exiv2.org/builds/exiv2-0.27.1-Linux64.tar.gz>
2. install `g++`
3. Copy `api.cpp` into the directory of exiv2 project.
    - Modify its contents:

    ```C++
    #define API extern "C" // on Linux
    //#define API extern "C" __declspec(dllexport) // on Windows
    ```

4. Execute compile command, to generate dynamic library.

    ```cmd
    g++ -std=c++98 api.cpp -o api.so -shared -fPIC -I $PWD/include -L $PWD/lib -l exiv2
    ```

5. Copy `lib/libexiv2.so` and `api.so` here.

---

## compile steps of api.dll on Windows (exiv2-0.27.2  requires Visual Studio 2017)

1. Download the source  https://www.exiv2.org/builds/exiv2-0.27.2-Source.tar.gz and extract to 
   `c:\......\exiv2-0.27.2-Source`  such that there the source for exiv2 can be found in  `c:\......\exiv2-0.27.2-Source\src`
2. Install `Visual Studio 2017` community edition is sufficient with Windows10 sdk, 
3. Set the environment variables it needs it  `C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat`
4. follow procedures in exiv2 for conan install https://github.com/Exiv2/exiv2/blob/master/README-CONAN.md#2-2 using example of profile `msvc2017Release64` using `c:\......\exiv2-0.27.2-Source` as the root folder
5. create build folder `mkdir c:\......\exiv2-0.27.2-Source\build` it will be on same level as `src` 
6. `cd c:\......\exiv2-0.27.2-Source\build`  and build exiv2

```
c:\....\exiv2\build> conan install .. --profile msvc2017Release64 --build missing
c:\....\exiv2\build> cmake         .. -G "Visual Studio 15 2017 Win64"
c:\....\exiv2\build> cmake --build .  --config Release
```


7. Copy `api.cpp` into the build directory of exiv2 `c:\....\exiv2\build` project.
    - Modify its contents:

    ```C++
    //#define API extern "C" // on Linux
    #define API extern "C" __declspec(dllexport) // on Windows
    ```

8. Open the CMD window, set the environment variables of exiv2 project.

    ```cmd
    cd <exiv2_dir>\bin
    set PATH=%CD%;%PATH%
    ```

9.  Run `vcvars64.bat` to initialize the DOS environment, like this:

    ```cmd
    C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvars64.bat
    ```

10.  Execute compile command, to generate dynamic library.

    ```cmd
    cl /MD /LD api.cpp /EHsc -I ..\include /link lib/release/exiv2.lib
    ``` 

11.  Copy `exiv2.dll` and `api.dll` to the `..\pyexiv2\pyexiv2\lib` folder

## compile steps of api.dll on Windows (exiv2-0.27.1  and Visual Studio 2015)

1. Download the release version of exiv2 project.
    - msvc64 : <https://www.exiv2.org/builds/exiv2-0.27.1-msvc64.zip>
2. Install `Visual Studio 2015`, and set the environment variables it needs.
3. Copy `api.cpp` into the directory of exiv2 project.
    - Modify its contents:

    ```C++
    //#define API extern "C" // on Linux
    #define API extern "C" __declspec(dllexport) // on Windows
    ```

4. Open the CMD window, set the environment variables of exiv2 project.

    ```cmd
    cd <exiv2_dir>\bin
    set PATH=%CD%;%PATH%
    ```

5. Run `vcvars64.bat` to initialize the DOS environment, like this:

    ```cmd
    "C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\amd64\vcvars64.bat"
    ```

6. Execute compile command, to generate dynamic library.

    ```cmd
    cl /MD /LD api.cpp /EHsc -I include /link lib/exiv2.lib
    ```

7. Copy `exiv2.dll` and `api.dll` here.

