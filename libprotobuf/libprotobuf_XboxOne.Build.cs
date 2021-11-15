// Copyright 1998-2017 Epic Games, Inc. All Rights Reserved.
using UnrealBuildTool;
using System.IO;

public class libprotobuf_XboxOne : libprotobuf
{
	public libprotobuf_XboxOne(ReadOnlyTargetRules Target) : base(Target)
	{
		Type = ModuleType.External;

		string protobufPath = ModuleDirectory;
		
		PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "xboxone", "protobuf.lib"));
		PublicSystemIncludePaths.Add(Path.Combine(protobufPath, "include"));
	}
}
