using UnrealBuildTool;
using System;
using System.IO;
using System.Collections.Generic;

public class libprotobuf : ModuleRules
{
	public libprotobuf(ReadOnlyTargetRules Target) : base(Target)
	{
		Type = ModuleType.External;

		string protobufPath = ModuleDirectory;

		bool is_supported = false;
		if (Target.Platform == UnrealTargetPlatform.Win64)
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "win64", "libprotobuf.lib"));
		}
		else if(Target.Platform == UnrealTargetPlatform.Linux)
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "linux", "libprotobuf.a"));
		}
		else if(Target.Platform == UnrealTargetPlatform.Android)
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "android", "libprotobuf.a"));
		}
		else if(Target.Platform == UnrealTargetPlatform.Mac)
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "mac", "libprotobuf.a"));
		}
		else if(Target.Platform == UnrealTargetPlatform.IOS)
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "ios", "libprotobuf.a"));
		}

		if (is_supported)
		{
			PublicSystemIncludePaths.Add(Path.Combine(protobufPath, "include"));
		}
	}
}

