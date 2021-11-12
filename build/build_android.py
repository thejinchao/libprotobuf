#-*- coding: utf-8 -*-
import subprocess
import os
import sys
import shutil
import build_common

android_sdk_home    = os.environ["ANDROID_HOME"]
android_ndk_root = os.environ["NDK_ROOT"]
cmake_path = os.path.join(android_sdk_home, "cmake", "3.10.2.4988404", "bin")
cmake_exe = os.path.join(cmake_path, "cmake.exe")
ninja_exe = os.path.join(cmake_path, "ninja.exe")
cmake_toolchain = os.path.join(android_ndk_root, "build", "cmake", "android.toolchain.cmake")

ndk_intermediate     = "_ndk_tmp"
protobuf_src_path   = "../../protobuf-source"
libprotobuf_path    = "../../libprotobuf"
install_path         = "_install"

def create_ninjia_prj():
	cmd_line = ["cmake.exe", "-G", "Ninja"]
	cmd_line.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(os.getcwd(), install_path))
	cmd_line.append("-DCMAKE_TOOLCHAIN_FILE="+cmake_toolchain)
	cmd_line.append("-DCMAKE_MAKE_PROGRAM="+ninja_exe)
	cmd_line.append("-Dprotobuf_BUILD_TESTS=false")
	cmd_line.append("-Dprotobuf_WITH_ZLIB=false")
	cmd_line.append(protobuf_src_path+"/cmake")
	subprocess.call(cmd_line)

def copy_library():
	target_include = os.path.join(libprotobuf_path, "include")
	if(os.path.exists(target_include)):
		shutil.rmtree(target_include, True)
	shutil.copytree(os.path.join(install_path, "include"), target_include)
	
	target_lib = os.path.join(libprotobuf_path, "lib/android");
	if(os.path.exists(target_lib)):
		shutil.rmtree(target_lib, True)
	os.makedirs(target_lib)
	shutil.copy(os.path.join(install_path, "lib/libprotobuf.a"), os.path.join(target_lib, "libprotobuf.a"))

##################################################
if __name__ == "__main__":
	#create intermediate path
	if not os.path.exists(ndk_intermediate):
		os.mkdir(ndk_intermediate)
		os.chdir(ndk_intermediate)
	else :
		os.chdir(ndk_intermediate)

	#apply patch
	if(build_common.apply_patch() != 0):
		print("Can't apply source patch!")
		exit(-1)
	
	#create ninja project files
	create_ninjia_prj()

	#build project 
	subprocess.call(ninja_exe)
	subprocess.call([ninja_exe, "install"])

	#copy library files
	copy_library()

	exit(0)
