libprotobuf for [Unreal Engine 4][]
=====

Link the google's `protocol bufffers` library as the third party in [Unreal Engine 4][].

Usage
-----

1. Import or copy the folder 'libprotobuf' into `<your project>/ThirdParty/libprotobuf`.
1. Add the libprotobuf as a module into `<your project>.Build.cs`
  * `PrivateDependencyModuleNames.AddRange(new string[] { "CoreUObject", "Engine", "libprotobuf" });`
1. Generate two code files (header & source, ex: Message.pb.h & Message.pb.cc) of the protocal by `protoc` for `cpp`. (Ref: [Google's Protocol Buffers][])
1. Put them into the source directory (`Private` or `Public`) of your project.
1. Regenerate the code file for [Unreal Engine 4][] by `regenerateforue4.py`.
    * `python regenerateforue4.py 'the header file'`
    * ex: `python regenerateforue4.py Message.pb.h`
    * You should get this information: `Success to regenerate the code for UE4`
1. Include and use the header file(ex: Message.pb.h) in your `.cpp` file.
1. That's all.

Build Library
-----
1. Windows: Run `build_win64.py` (Visual Studio 2015 and [CMake][] is required)
1. Linux: Run `build_linux.py` ([clang][] and Unrea Engine Source Code is required)

Reference
-----
1. https://github.com/code4game/libprotobuf
1. https://wiki.unrealengine.com/Standalone_Dedicated_Server
1. https://wiki.unrealengine.com/Linking_Static_Libraries_Using_The_Build_System


[Unreal Engine 4]: https://www.unrealengine.com/
[Google's Protocol Buffers]: https://developers.google.com/protocol-buffers/
[CMake]:http://www.cmake.org
[clang]:https://wiki.unrealengine.com/Compiling_For_Linux
