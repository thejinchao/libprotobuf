# This file is copy from https://github.com/code4game/libprotobuf
# Copyright @ 2016, Code 4 Game, Under The MIT License.

from datetime import *
import os
import sys

msvc_check_begin = '#ifdef _MSC_VER'
msvc_check_end   = '#endif'
comment = '// Added for UE4 in {0}(UTC)'.format(datetime.utcnow())
include_allow_header = '#include "AllowWindowsPlatformTypes.h"'
include_hide_header = '#include "HideWindowsPlatformTypes.h"'

def Check(_CodeFile):
    if (os.path.isfile(_CodeFile) is False):
        print "Can't find the code file!!!"
        return False

    code_file = open(_CodeFile, 'r')
    if (code_file is None):
        print "Failed to read the code file!!!"
        return False
    code_lines = code_file.readlines()
    code_file.close()

    for line in code_lines[:10]:
        if (line.find(include_allow_header) < 0 and line.find(include_hide_header) < 0):
            continue
        print "Already was regenerated?"
        return False
    return True

def Generate(_CodeFile):
    if (Check(_CodeFile) is False):
        print "Failed to check the code file!!!"
        return

    if (os.path.isfile(_CodeFile) is False):
        print "Can't find the code file!!!"
        return

    code_file = open(_CodeFile, 'r')
    if (code_file is None):
        print "Failed to read the code file!!!"
        return
    code_lines = code_file.readlines()
    code_file.close()

    code_file = open(_CodeFile, 'w')
    if (code_file is None):
        print "Failed to write the code file!!!"
        return
    meet_first_include = False
    meet_last_include = False
    for line in code_lines:
        if (meet_first_include is False and (line[0:10] == "#include \"" or line[0:10] == "#include <" )):
            code_file.write('\n{0}\n{1} {2}\n{3}\n\n'.format(msvc_check_begin, include_allow_header, comment, msvc_check_end))
            meet_first_include = True
        code_file.write(line)
        if (meet_last_include is False and line[:len(line) - 1] == "// @@protoc_insertion_point(includes)"):
            code_file.write('\n{0}\n{1} {2}\n{3}\n\n'.format(msvc_check_begin, include_hide_header, comment, msvc_check_end))
            meet_last_include = True
    code_file.close()
    if (meet_first_include is False):
        print "Can't add the allow header!!!"
    if (meet_last_include is False):
        print "Can't add the hide header!!!"
    if (meet_first_include and meet_last_include):
        print "Success to regenerate the code for UE4"

if len(sys.argv) <= 1:
    print "Usage: python regenerateforue4.py `code file`"
else:
    Generate(sys.argv[1])
