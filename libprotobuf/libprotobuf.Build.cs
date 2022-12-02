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
		if (Target.Platform.ToString() == "Win64")
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "win64", 
				ConfigurationDir(Target.Configuration), "libprotobuf.lib"));
		}
		else if(Target.Platform.ToString() == "Linux")
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "linux",
				ConfigurationDir(Target.Configuration), "libprotobuf.a"));
		}
		else if(Target.Platform.ToString() == "Android")
		{
			is_supported = true;
			List<String> Architectures = new List<String> { "armeabi-v7a", "arm64-v8a", "x86_64" };
			foreach(var arch in Architectures) {
				PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "android", arch,
					ConfigurationDir(Target.Configuration), "libprotobuf.a"));
			}
		}
		else if(Target.Platform.ToString() == "Mac")
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "mac", "libprotobuf.a"));
		}
		else if(Target.Platform.ToString() == "IOS")
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "ios", "libprotobuf.a"));
		}
		else if (Target.Platform.ToString() == "PS4")
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "ps4",
				ConfigurationDir(Target.Configuration), "libprotobuf.a"));
		}
		else if (Target.Platform.ToString() == "PS5")
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "ps5",
				ConfigurationDir(Target.Configuration), "libprotobuf.a"));
		}

		if (is_supported)
		{
			PublicSystemIncludePaths.Add(Path.Combine(protobufPath, "include"));
		}
	}

	public string ConfigurationDir(UnrealTargetConfiguration Configuration)
	{
		if (Configuration == UnrealTargetConfiguration.Debug || Configuration == UnrealTargetConfiguration.DebugGame)
		{
			return "Debug";
		}
		else
		{
			return "Release";
		}
	}
}

