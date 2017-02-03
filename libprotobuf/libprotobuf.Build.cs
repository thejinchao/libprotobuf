// Jinchao: This file is copy from https://github.com/code4game/libprotobuf
// Copyright 2016 Code 4 Game. All Rights Reserved.

using UnrealBuildTool;

public class libprotobuf : ModuleRules
{
    public libprotobuf(TargetInfo Target)
    {
        Type = ModuleType.External;

        bool is_supported = false;
        if (Target.Platform == UnrealTargetPlatform.Win64)
        {
            is_supported = true;

            string protobuf_lib_directory_full_path = System.IO.Path.Combine(ModuleDirectoryFullPath, "lib", "win64");
            PublicLibraryPaths.Add(protobuf_lib_directory_full_path);
            PublicAdditionalLibraries.Add("libprotobuf.lib");

            Definitions.AddRange(
                new string[]
                {
                    "WIN64",
                    "_WINDOWS",
                    "NDEBUG",
                    "GOOGLE_PROTOBUF_CMAKE_BUILD",
                });
        }
        else if(Target.Platform == UnrealTargetPlatform.Linux)
        {
            is_supported = true;

            string protobuf_lib_directory_full_path = System.IO.Path.Combine(ModuleDirectoryFullPath, "lib", "linux");
            PublicLibraryPaths.Add(protobuf_lib_directory_full_path);
            PublicAdditionalLibraries.Add("protobuf");

            Definitions.AddRange(
                new string[]
                {
                    "GOOGLE_PROTOBUF_NO_RTTI=1",
                });
        }
        
        if (is_supported)
        {
            string protobuf_code_directory_full_path = System.IO.Path.Combine(ModuleDirectoryFullPath, "include");

            PublicSystemIncludePaths.Add(protobuf_code_directory_full_path);
        }
    }

    string ModuleDirectoryFullPath
    {
        get { return System.IO.Path.GetFullPath(ModuleDirectory); }
    }
}

