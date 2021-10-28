#-*- coding: utf-8 -*-
import subprocess
import os
import sys
import shutil

def apply_patch():
	current_file=os.path.abspath(__file__)
	patch_file=os.path.join(os.path.dirname(current_file), "patch", "diff-base-on-3.19.0.diff")
	print("patch_file=%s" % patch_file)

	source_path = os.path.join(os.path.dirname(os.path.dirname(current_file)), "protobuf-source")
	print("source_path=%s" % source_path)

	cmd_line = ["git", "apply", patch_file]
	p = subprocess.Popen(cmd_line, cwd=source_path)
	p.wait()
	return p.returncode


