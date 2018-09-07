import subprocess
import os
import sys
import shutil

vs_intermediate     = "_vs_tmp"
protobuf_src_path   = "../../protobuf-source"
libprotobuf_path    = "../../libprotobuf"
prefix_path         = "_prefix"

def create_vs_prj():
    cmd_line = ["cmake", "-G", "Visual Studio 15 2017 Win64"]
    #install prefix
    cmd_line.append("-DCMAKE_INSTALL_PREFIX="+os.path.join(os.getcwd(), prefix_path))
    cmd_line.append("-DCMAKE_CONFIGURATION_TYPES=Release")
    cmd_line.append("-Dprotobuf_BUILD_TESTS=false")
    cmd_line.append("-Dprotobuf_MSVC_STATIC_RUNTIME=false")
    cmd_line.append("-Dprotobuf_WITH_ZLIB=false")
    cmd_line.append(protobuf_src_path+"/cmake")
    subprocess.call(cmd_line)


def get_vs2017_devenv():
    try:
        vswhere = os.path.join(os.environ.get('ProgramFiles(x86)'), "Microsoft Visual Studio/Installer/vswhere.exe")
        vswhere_process = subprocess.Popen([vswhere,'-latest', '-version',  '[15.0,16.0)', '-property', 'installationPath', '-nologo'], shell=False, stdout=subprocess.PIPE)
        while vswhere_process.poll() is None:
            line = vswhere_process.stdout.readline().strip().decode("utf-8")
            devenv_com = os.path.join(line, "Common7/IDE/devenv.com")
            if(os.path.exists(devenv_com)) :
                return devenv_com
            else :
                print(line)
                return None
        return None
    except:
        return None

   
def copy_library():
    target_include = os.path.join(libprotobuf_path, "include")
    if(os.path.exists(target_include)):
        shutil.rmtree(target_include, True)
    shutil.copytree(os.path.join(prefix_path, "include"), target_include)
    
    target_bin = os.path.join(libprotobuf_path, "bin")
    if(os.path.exists(target_bin)):
        shutil.rmtree(target_bin, True)
    shutil.copytree(os.path.join(prefix_path, "bin"), target_bin)
    
    target_lib = os.path.join(libprotobuf_path, "lib/win64");
    if(os.path.exists(target_lib)):
        shutil.rmtree(target_lib, True)
    os.makedirs(target_lib)
    shutil.copy(os.path.join(prefix_path, "lib/libprotobuf.lib"), os.path.join(libprotobuf_path, "lib/win64/libprotobuf.lib"))
    
##################################################

#create intermediate path
if os.path.exists(vs_intermediate):
    shutil.rmtree(vs_intermediate, True)
os.mkdir(vs_intermediate)
os.chdir(vs_intermediate)


#create vs project files
create_vs_prj()

#build vs project 
devenv_path = get_vs2017_devenv()
if(devenv_path is None) :
    print("Visual Studio 2017 not found!")
    os._exit(0)
print("Build protobuf...")    
subprocess.call([devenv_path, "protobuf.sln", "/Build", "Release|x64", "/Project", "INSTALL"])


#copy library files
copy_library()
