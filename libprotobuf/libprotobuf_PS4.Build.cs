// Copyright 1998-2017 Epic Games, Inc. All Rights Reserved.
using UnrealBuildTool;
using System.IO;

public class libprotobuf_PS4 : libprotobuf
{
	public libprotobuf_PS4(ReadOnlyTargetRules Target) : base(Target)
	{
		Type = ModuleType.External;

		string protobufPath = ModuleDirectory;
		
		PublicAdditionalLibraries.Add(Path.Combine(protobufPath, "lib", "ps4", "libprotobuf.a"));
		PublicSystemIncludePaths.Add(Path.Combine(protobufPath, "include"));
	}
}
