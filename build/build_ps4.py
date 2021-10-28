#-*- coding: utf-8 -*-
import subprocess
import os
import sys
import shutil
import build_common

build_intermediate     = "_ps4_tmp"
protobuf_src_path   = "../../protobuf-source"
libprotobuf_path    = "../../libprotobuf"
install_path         = "_install"

def create_vs_prj():
	ps4_cmake=os.path.join(os.getenv("SCE_ROOT_DIR"), "ORBIS", "Tools", "CMake", "PS4CMake.bat")
	if(not os.path.isfile(ps4_cmake)):
		print("Can't find PS4CMake.bat '%s'")
		return -1;
	print("Find PS4 CMake batch file '%s'" % ps4_cmake)
	cmd_line = [ps4_cmake]
	cmd_line.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(os.getcwd(), install_path))
	cmd_line.append("-Dprotobuf_BUILD_TESTS=false")
	cmd_line.append("-Dprotobuf_MSVC_STATIC_RUNTIME=false")
	cmd_line.append("-Dprotobuf_WITH_ZLIB=false")
	cmd_line.append("-Dprotobuf_BUILD_EXAMPLES=false")
	cmd_line.append("-Dprotobuf_BUILD_PROTOC_BINARIES=false")
	cmd_line.append("-Dprotobuf_BUILD_LIBPROTOC=false")
	cmd_line.append("-Dprotobuf_DISABLE_RTTI=true")
	cmd_line.append(protobuf_src_path+"/cmake")
	subprocess.call(cmd_line)

def copy_library():
	target_include = os.path.join(libprotobuf_path, "include")
	if(os.path.exists(target_include)):
		shutil.rmtree(target_include, True)
	shutil.copytree(os.path.join(install_path, "include"), target_include)
	
	target_lib = os.path.join(libprotobuf_path, "lib/ps4");
	if(os.path.exists(target_lib)):
		shutil.rmtree(target_lib, True)
	os.makedirs(target_lib)
	shutil.copy(os.path.join(install_path, "lib/libprotobuf.a"), os.path.join(libprotobuf_path, "lib/ps4/libprotobuf.a"))

##################################################
if __name__ == "__main__":
	#create intermediate path
	if not os.path.exists(build_intermediate):
		os.mkdir(build_intermediate)
		os.chdir(build_intermediate)
	else :
		os.chdir(build_intermediate)
	
	#apply patch
	if(build_common.apply_patch() != 0):
		print("Can't apply source patch!")
		exit(-1)
	
	#create vs project files
	create_vs_prj()
	
	#build vs project 
	subprocess.call(["cmake", "--build", ".", "--config", "Release", "--target", "INSTALL"])
	
	#copy library files
	copy_library()
	
	exit(0)
