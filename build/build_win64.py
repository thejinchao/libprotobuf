#-*- coding: utf-8 -*-
import subprocess
import os
import sys
import shutil

vs_intermediate     = "_vs_tmp"
protobuf_src_path   = "../../protobuf-source"
libprotobuf_path    = "../../libprotobuf"
install_path         = "_install"

def apply_patch():
	current_file=os.path.abspath(__file__)
	patch_file=os.path.join(os.path.dirname(current_file), "patch", "win64", "diff-base-on-3.19.0.diff")
	print("patch_file=%s" % patch_file)

	source_path = os.path.join(os.path.dirname(os.path.dirname(current_file)), "protobuf-source")
	print("source_path=%s" % source_path)

	cmd_line = ["git", "apply", patch_file]
	p = subprocess.Popen(cmd_line, cwd=source_path)
	p.wait()
	return p.returncode
	
def create_vs_prj():
	cmd_line = ["cmake", "-G", "Visual Studio 16 2019", "-A", "x64"]
	cmd_line.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(os.getcwd(), install_path))
	cmd_line.append("-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
	cmd_line.append("-Dprotobuf_BUILD_TESTS=false")
	cmd_line.append("-Dprotobuf_MSVC_STATIC_RUNTIME=false")
	cmd_line.append("-Dprotobuf_WITH_ZLIB=false")
	cmd_line.append(protobuf_src_path+"/cmake")
	subprocess.call(cmd_line)

def copy_library():
	target_include = os.path.join(libprotobuf_path, "include")
	if(os.path.exists(target_include)):
		shutil.rmtree(target_include, True)
	shutil.copytree(os.path.join(install_path, "include"), target_include)
	
	target_bin = os.path.join(libprotobuf_path, "bin")
	if(os.path.exists(target_bin)):
		shutil.rmtree(target_bin, True)
	shutil.copytree(os.path.join(install_path, "bin"), target_bin)
	
	target_lib = os.path.join(libprotobuf_path, "lib/win64");
	if(os.path.exists(target_lib)):
		shutil.rmtree(target_lib, True)
	os.makedirs(target_lib)
	shutil.copy(os.path.join(install_path, "lib/libprotobuf.lib"), os.path.join(libprotobuf_path, "lib/win64/libprotobuf.lib"))

##################################################
if __name__ == "__main__":
	#create intermediate path
	if not os.path.exists(vs_intermediate):
		os.mkdir(vs_intermediate)
		os.chdir(vs_intermediate)
	else :
		os.chdir(vs_intermediate)
		shutil.rmtree(install_path, True)

	#apply patch
	if(apply_patch() != 0):
		print("Can't apply source patch!")
		exit(-1)
	
	#create vs project files
	create_vs_prj()

	#build vs project 
	subprocess.call(["cmake", "--build", ".", "--config", "Release", "--target", "INSTALL"])

	#copy library files
	copy_library()

	exit(0)
