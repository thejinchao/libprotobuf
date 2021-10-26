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
			Definitions.AddRange(
				new string[]{
					"GOOGLE_PROTOBUF_INTERNAL_DONATE_STEAL_INLINE=0",
				});
		}
		else if(Target.Platform == UnrealTargetPlatform.Linux)
		{
			is_supported = true;
			PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "linux", "libprotobuf.lib"));
/*
            Definitions.AddRange(
                new string[]
                {
                    "GOOGLE_PROTOBUF_NO_RTTI=1",
                });
*/				
		}

		if (is_supported)
		{
			PublicSystemIncludePaths.Add(Path.Combine(protobufPath, "include"));
		}
	}
}

