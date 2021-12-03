libprotobuf for [Unreal Engine 4][]
=====

Link the google's `protocol bufffers` library as the third party in [Unreal Engine 4][].

# Version
* [Protobuf][]: 3.19.0
* [Unreal Engine 4][]: 4.27.1

# Usage
1. Import or copy the folder `libprotobuf` into `<your project>/Source/ThirdParty/libprotobuf`.
1. Add the libprotobuf as a module into `<your project>.Build.cs`
  ```C++
  PrivateDependencyModuleNames.AddRange(new string[] { "libprotobuf" });
  ```

# Compile proto file(s)
1. Compile the proto files for [Unreal Engine 4][] by `generate_for_ue4.py`.
    * `python generate_for_ue4.py --proto_input <proto_file_or_path> --cpp_out <output_path>`
    * ex: `python generate_for_ue4.py --proto_input Message.proto --cpp_out d:\Prject\Source\ProtoFiles`
1. Include and use the header file(ex: Message.pb.h) in your `.cpp` file.

# Build Library
Apply the patch first
```
cd <prj_root>\protobuf-source
git apply ..\build\patch\diff-base-on-3.19.0.diff
```

## 1. Windows
[Visual Studio 2019](https://visualstudio.microsoft.com/) and [CMake][] are required
```
cd <prj_root>/build
mkdir _win64 & cd _win64
cmake -G "Visual Studio 16 2019" -A x64 ..\..\protobuf-source\cmake ^
 -DCMAKE_INSTALL_PREFIX=_install ^
 -DCMAKE_MSVC_RUNTIME_LIBRARY="MultiThreaded$<$<CONFIG:Debug>:Debug>DLL" ^
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false ^
 -Dprotobuf_MSVC_STATIC_RUNTIME=false
 
cmake --build . --target install --config Release
```
## 2. Linux(Cross Compiling)
[Clang cross-compile toolchain][], [Ninja][] and Unreal Engine Source Code are required
```
cd <prj_root>/build
mkdir _linux & cd _linux
cmake -G "Ninja" ..\..\protobuf-source\cmake ^
 -DCMAKE_MAKE_PROGRAM=<ninja_install_path>\ninja.exe ^
 -DCMAKE_TOOLCHAIN_FILE="..\linux\ue4-linux-cross-compile.cmake" ^
 -DCMAKE_INSTALL_PREFIX=_install ^
 -DUE4_ENGINE_PATH=<ue4_source_path>\Engine ^
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false ^
 -Dprotobuf_BUILD_EXAMPLES=false ^
 -Dprotobuf_BUILD_PROTOC_BINARIES=false -Dprotobuf_BUILD_LIBPROTOC=false

cmake --build . --target install --config Release
```

## 3. Android
[Android Studio](https://developer.android.com/studio) is required. And you need install other additional sdk and tools through `SDK Manager`. 
* Android NDK: r21b(21.4.7075529)
* Android SDK Build-Tools: 28.0.3
* Android SDK Command-line Tools
* CMake

Obtaining the correct component version is important. you can get the version info from this file: `Engine\Extras\Android\SetupAndroid.bat`
```
cd <prj_root>/build
mkdir _android & cd _android
"%ANDROID_HOME%\cmake\X.XX.X\bin\cmake.exe" -G "Ninja" ..\..\protobuf-source\cmake ^
 -DCMAKE_INSTALL_PREFIX=_install ^
 -DCMAKE_TOOLCHAIN_FILE="%NDK_ROOT%\build\cmake\android.toolchain.cmake" ^
 -DCMAKE_MAKE_PROGRAM=%ANDROID_HOME%\cmake\X.XX.X\bin\ninja.exe ^
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false ^
 -Dprotobuf_BUILD_EXAMPLES=false ^
 -Dprotobuf_BUILD_PROTOC_BINARIES=false -Dprotobuf_BUILD_LIBPROTOC=false

"%ANDROID_HOME%\cmake\X.XX.X\bin\cmake.exe" --build . --target install --config Release
```

## 4. PlayStation 4
PS4 SDK(Orbis) is required.
```
cd <prj_root>/build
mkdir _ps4 & cd _ps4
"%SCE_ROOT_DIR%\ORBIS\Tools\CMake\PS4CMake.bat" ..\..\protobuf-source\cmake ^
 -DCMAKE_INSTALL_PREFIX=_install ^
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false ^
 -Dprotobuf_BUILD_EXAMPLES=false ^
 -Dprotobuf_BUILD_PROTOC_BINARIES=false -Dprotobuf_BUILD_LIBPROTOC=false ^
 -Dprotobuf_DISABLE_RTTI=true

cmake --build . --target install --config Release
```

## 5. PlayStation 5
PS5 SDK(Prospero) is required.
```
cd <prj_root>/build
mkdir _ps5 & cd _ps5
"%SCE_ROOT_DIR%\Prospero\Tools\CMake\PS5CMake.bat" ..\..\protobuf-source\cmake ^
 -DCMAKE_INSTALL_PREFIX=_install ^
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false ^
 -Dprotobuf_BUILD_EXAMPLES=false ^
 -Dprotobuf_BUILD_PROTOC_BINARIES=false -Dprotobuf_BUILD_LIBPROTOC=false ^
 -Dprotobuf_DISABLE_RTTI=true

cmake --build . --target install --config Release
```

## 6. Mac
Xcode and CMake are required.
```
cd <prj_root>/build
mkdir _mac && cd _mac
cmake -G "Unix Makefiles" ../../protobuf-source/cmake \
 -DCMAKE_INSTALL_PREFIX=./_install \
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false \
 -Dprotobuf_BUILD_EXAMPLES=false \
 -Dprotobuf_BUILD_PROTOC_BINARIES=false -Dprotobuf_BUILD_LIBPROTOC=false \
 -DCMAKE_OSX_DEPLOYMENT_TARGET=10.14 
 
cmake --build . --target install --config Release
```
## 7. iOS
Xcode and CMake are required.
```
cd <prj_root>/build
mkdir _ios && cd _ios
cmake -G "Unix Makefiles" ../../protobuf-source/cmake \
-DCMAKE_INSTALL_PREFIX=./_install \
-DCMAKE_TOOLCHAIN_FILE=../ios/ios.toolchain.cmake -DPLATFORM=OS64 \
 -Dprotobuf_BUILD_TESTS=false -Dprotobuf_WITH_ZLIB=false \
 -Dprotobuf_BUILD_EXAMPLES=false \
 -Dprotobuf_BUILD_PROTOC_BINARIES=false -Dprotobuf_BUILD_LIBPROTOC=false 

cmake --build . --target install --config Release
```

# License
Use The MIT License.

# Reference
1. https://github.com/code4game/libprotobuf
1. https://unrealcommunity.wiki/standalone-dedicated-server-i5qjfc27
1. https://unrealcommunity.wiki/linking-static-libraries-using-the-build-system-1ahhe4vt
1. https://unrealcommunity.wiki/compiling-for-linux-nutp04d0
1. https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/Linux/

[Unreal Engine 4]: https://www.unrealengine.com/
[Protobuf]: https://github.com/protocolbuffers/protobuf
[CMake]:http://www.cmake.org
[Ninja]:https://ninja-build.org
[Clang cross-compile toolchain]:https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/Linux/GettingStarted/
