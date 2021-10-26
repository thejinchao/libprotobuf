#-*- coding: utf-8 -*-
import os
import sys
import io
import subprocess
import shutil
from argparse import ArgumentParser

cpp_fixed_line="/*@ fixed */"
avoid_msvc_warning_in_cpp = '''
#if defined(_MSC_VER)
  #pragma warning (disable:4018) // 'expression' : signed/unsigned mismatch
  #pragma warning (disable:4065) // switch statement contains 'default' but no 'case' labels
  #pragma warning (disable:4146) // unary minus operator applied to unsigned type, result still unsigned
  #pragma warning (disable:4244) // 'conversion' conversion from 'type1' to 'type2', possible loss of data
  #pragma warning (disable:4251) // 'identifier' : class 'type' needs to have dll-interface to be used by clients of class 'type2'
  #pragma warning (disable:4267) // 'var' : conversion from 'size_t' to 'type', possible loss of data
  #pragma warning (disable:4305) // 'identifier' : truncation from 'type1' to 'type2'
  #pragma warning (disable:4307) // 'operator' : integral constant overflow
  #pragma warning (disable:4309) // 'conversion' : truncation of constant value
  #pragma warning (disable:4334) // 'operator' : result of 32-bit shift implicitly converted to 64 bits (was 64-bit shift intended?)
  #pragma warning (disable:4355) // 'this' : used in base member initializer list
  #pragma warning (disable:4506) // no definition for inline function 'function'
  #pragma warning (disable:4800) // 'type' : forcing value to bool 'true' or 'false' (performance warning)
  #pragma warning (disable:4996) // The compiler encountered a deprecated declaration.
  #pragma warning (disable:4125) // decimal digit terminates octal escape sequence
#endif
'''

avoid_msvc_warning_in_h = '''
#if defined(_MSC_VER)
  #pragma warning (disable:4946) // reinterpret_cast used between related classes: 'class1' and 'class2'
#endif
'''

def get_protoc_exe():
	current_file=os.path.abspath(__file__)
	sdk_bin_path=os.path.join(os.path.dirname(os.path.dirname(current_file)), "bin")
	protoc_file=os.path.join(sdk_bin_path, "protoc.exe")
	if(os.path.isfile(protoc_file)):
		return protoc_file
	print("Can't find 'protoc.exe' in '%s'!" % sdk_bin_path)
	return None

def walk_tree(top_most_path, relative_path, ext_filter, file_list):
	current_path = os.path.join(top_most_path, relative_path)
	for f in os.listdir(current_path):
		pathname = os.path.join(current_path, f)
		if(os.path.isfile(pathname)):
			fullname = os.path.realpath(pathname)
			[dirname, filename]=os.path.split(fullname)
			filename_ext = os.path.splitext(filename)[1]
			if(filename_ext.lower() != ext_filter):
				continue
			file_list.append(os.path.join(relative_path, f))
		elif(os.path.isdir(pathname)):
			walk_tree(top_most_path, os.path.join(relative_path, f), ext_filter, file_list)

def update_cpp_file(input_file_name, content):
	fullname = os.path.realpath(input_file_name)
	file_handle = open(fullname, "r")
	if(file_handle==None):
		print("Open %s failed!"%fullname)
		return 1
	first_line = file_handle.readline()
	if(first_line[0:len(cpp_fixed_line)] == cpp_fixed_line):
		#already done
		file_handle.close()
		return 2
	other_content = file_handle.read()
	file_handle.close()
	
	#write file
	file_handle = io.open(fullname, "w", newline="\n")
	if(file_handle==None):
		print("Write %s failed!"%fullname)
		return 1
	file_handle.write(u"%s\n" % cpp_fixed_line)
	file_handle.write(u"%s" % content)
	file_handle.write(u'{}'.format(first_line))
	file_handle.write(u'{}'.format(other_content))
	file_handle.close()
	return 0

def build_proto_file(protoc, proto_path, proto_file, cpp_out):
	print("build proto file '%s'" % proto_file)
	
	abs_proto_path=os.path.realpath(proto_path)
	abs_cpp_out=os.path.realpath(cpp_out)
	cmd = "\"%s\" --cpp_out=\"%s\" --proto_path=\"%s\" \"%s\"" % (protoc, abs_cpp_out, abs_proto_path, proto_file)
	p = subprocess.Popen(cmd, cwd=abs_proto_path)
	p.wait()
	if(p.returncode!=0):
		return p.returncode
	
	# avoid msvc warning
	filename_portion=os.path.splitext(proto_file)
	cpp_file = os.path.join(abs_cpp_out, filename_portion[0]+".pb.cc")
	ret = update_cpp_file(cpp_file, avoid_msvc_warning_in_cpp)
	if(ret != 0) : 
		return ret
	h_file = os.path.join(abs_cpp_out, filename_portion[0]+".pb.h")
	ret = update_cpp_file(h_file, avoid_msvc_warning_in_h)
	return ret

if __name__ == "__main__":
	parser = ArgumentParser(description="Compile Proto Files for UE4")
	parser.add_argument("--proto_input", required=True, help="proto file or path will be processed.")
	parser.add_argument("--cpp_out", help="the cpp output directory for cpp generator.")

	option = parser.parse_args()
	if (not(option.proto_input)) :
		parser.print_help()
		exit(0)
	
	cpp_out = os.getcwd()
	if(option.cpp_out):
		cpp_out = option.cpp_out
	print("cpp_out=%s" % cpp_out)
	
	#make sure cpp out is exist
	if(not os.path.exists(cpp_out)):
		os.mkdir(cpp_out)
		if(not os.path.exists(cpp_out)):
			print("Error, create '%s' failed" % cpp_out)
			exit(-1)
	
	protoc = get_protoc_exe()
	if(not protoc):
		exit(-1)
	print("protoc=%s" % protoc)
	
	if(os.path.isfile(option.proto_input)):
		fullname=os.path.realpath(option.proto_input)
		[dirname, filename]=os.path.split(fullname)
		ret = build_proto_file(protoc, dirname, filename, cpp_out)
		if(ret !=0):
			exit(ret)
	elif(os.path.isdir(option.proto_input)):
		proto_files=[]
		walk_tree(option.proto_input, "", ".proto", proto_files)
		for f in proto_files:
			ret = build_proto_file(protoc, option.proto_input, f, cpp_out)
			if(ret !=0):
				exit(ret)
	else:
		print("Can't open proto input '%s'", option.proto_input)
		exit(-1)
	#Done!
	print("Done!")
	exit(0)
