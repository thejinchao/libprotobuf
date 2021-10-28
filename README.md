libprotobuf for [Unreal Engine 4][]
=====

Link the google's `protocol bufffers` library as the third party in [Unreal Engine 4][].

Version
-----
* ProtoBuf: 3.19.0
* UnrealEngine: 4.27.1
* PS4 SDK: 9.008.001
* PS5 SDK: 4.00.00.43

Usage
-----

1. Import or copy the folder `libprotobuf` into `<your project>/Source/ThirdParty/libprotobuf`.
1. Add the libprotobuf as a module into `<your project>.Build.cs`
  ```C++
  PrivateDependencyModuleNames.AddRange(new string[] { "libprotobuf" });
  ```

Compile proto file(s)
-----
1. Compile the proto files for [Unreal Engine 4][] by `generate_for_ue4.py`.
    * `python generate_for_ue4.py --proto_input <proto_file_or_path> --cpp_out <output_path>`
    * ex: `python generate_for_ue4.py --proto_input Message.proto --cpp_out d:\Prject\Source\ProtoFiles`
1. Include and use the header file(ex: Message.pb.h) in your `.cpp` file.

Build Library
-----
1. Windows: Run `build_win64.py` (Visual Studio 2019 and [CMake][] is required)
1. Linux: Run `build_linux.py` ([clang][] and Unrea Engine Source Code is required)
1. PS4(Orbis): Run `build_ps4.py`(PS4 SDK and UnrealEngine PS4 Patch is required)
1. PS5(Prospero): Run `build_ps5.py`(PS5 SDK and UnrealEngine PS5 Patch is required)

License
-----
Use The MIT License.

Reference
-----
1. https://github.com/code4game/libprotobuf
1. https://unrealcommunity.wiki/standalone-dedicated-server-i5qjfc27
1. https://unrealcommunity.wiki/linking-static-libraries-using-the-build-system-1ahhe4vt
1. https://unrealcommunity.wiki/compiling-for-linux-nutp04d0
1. https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/Linux/

[Unreal Engine 4]: https://www.unrealengine.com/
[Google's Protocol Buffers]: https://developers.google.com/protocol-buffers/
[CMake]:http://www.cmake.org
[clang]:https://docs.unrealengine.com/4.27/en-US/SharingAndReleasing/Linux/GettingStarted/
