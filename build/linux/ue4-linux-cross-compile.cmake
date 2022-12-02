# A simple toolchain for Unreal Engine4 Linxu Compile toolchain

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR x86_64)
set(UNIX 1)

string (REPLACE "\\" "/" CLANG_MULTIARCH_ROOT "$ENV{LINUX_MULTIARCH_ROOT}")
set(LINUX_ARCH_NAME "${CMAKE_SYSTEM_PROCESSOR}-unknown-linux-gnu")

set(CLANG_TOOLCHAIN_ROOT "${CLANG_MULTIARCH_ROOT}/${LINUX_ARCH_NAME}")
if (NOT EXISTS "${CLANG_TOOLCHAIN_ROOT}")
	message(FATAL_ERROR "Path <${CLANG_TOOLCHAIN_ROOT}> does not exist")
endif()
message(STATUS "clang tool chain path: ${CLANG_TOOLCHAIN_ROOT}")
set(CLANG_TOOLCHAIN_BIN "${CLANG_TOOLCHAIN_ROOT}/bin")

message(STATUS "Configuring UE4 Linux cross-compile")

# =============================================================================
# Set file suffixes/prefixes
# =============================================================================
set(CMAKE_STATIC_LIBRARY_SUFFIX ".a")
set(CMAKE_STATIC_LIBRARY_SUFFIX_CXX ".a")

# =============================================================================
# Define cmake behaviors
# =============================================================================
set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(CMAKE_FIND_ROOT_PATH ${CLANG_TOOLCHAIN_ROOT})
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY BOTH)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE BOTH)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE BOTH)

# Optionally reduce compiler sanity check when cross-compiling.
set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

# =============================================================================
# Define tool paths
# =============================================================================
set(CMAKE_C_COMPILER	${CLANG_TOOLCHAIN_BIN}/clang.exe 							CACHE PATH "compiler" FORCE)
set(CMAKE_CXX_COMPILER	${CLANG_TOOLCHAIN_BIN}/clang++.exe							CACHE STRING "" FORCE)
set(CMAKE_ASM_COMPILER	${CMAKE_C_COMPILER}											CACHE STRING "" FORCE)
set(CMAKE_AR 			${CLANG_TOOLCHAIN_BIN}/x86_64-unknown-linux-gnu-ar.exe		CACHE PATH "archive")
set(CMAKE_RANLIB		${CLANG_TOOLCHAIN_BIN}/x86_64-unknown-linux-gnu-ranlib.exe	CACHE PATH "ranlib")
set(CMAKE_LINKER 		${CLANG_TOOLCHAIN_BIN}/x86_64-unknown-linux-gnu-ld.exe		CACHE PATH "linker")
set(CMAKE_NM 			${CLANG_TOOLCHAIN_BIN}/x86_64-unknown-linux-gnu-gcc-nm.exe	CACHE PATH "nm")
set(CMAKE_OBJCOPY 		${CLANG_TOOLCHAIN_BIN}/x86_64-unknown-linux-gnu-objcopy.exe	CACHE PATH "objcopy")
set(CMAKE_OBJDUMP 		${CLANG_TOOLCHAIN_BIN}/x86_64-unknown-linux-gnu-objdump.exe	CACHE PATH "objdump")

# =============================================================================
# Define flags 
# =============================================================================
set(COMPILER_FLAGS 		 " -nostdinc++ --target=${LINUX_ARCH_NAME} --sysroot='${CLANG_TOOLCHAIN_ROOT}' -fno-math-errno -fno-rtti -fno-exceptions -fdiagnostics-format=msvc -funwind-tables -gdwarf-3")
set(FLAGS_DEBUG 		 " -O0 -g -D_DEBUG")
set(FLAGS_MINSIZEREL 	 " -Os -DNDEBUG")
set(FLAGS_RELEASE 		 " -O3 -DNDEBUG")
set(FLAGS_RELWITHDEBINFO " -O3 -g -D_DEBUG")

# =============================================================================
# Define include paths
# =============================================================================
set(CMAKE_SYSTEM_INCLUDE_PATH "")
set(CMAKE_INCLUDE_PATH	"")

include_directories("${UE_THIRD_PARTY_PATH}/Linux/LibCxx/include/c++/v1")
include_directories("${CLANG_TOOLCHAIN_ROOT}/usr/include")


# =============================================================================
# Set compiler flags
# =============================================================================	
string(CONCAT CMAKE_CXX_FLAGS					"${CMAKE_CXX_FLAGS_INIT}				${COMPILER_FLAGS}")
string(CONCAT CMAKE_CXX_FLAGS_DEBUG				"${CMAKE_CXX_FLAGS_DEBUG_INIT}			${FLAGS_DEBUG}")
string(CONCAT CMAKE_CXX_FLAGS_MINSIZEREL		"${CMAKE_CXX_FLAGS_MINSIZEREL_INIT} 	${FLAGS_MINSIZEREL}")
string(CONCAT CMAKE_CXX_FLAGS_RELEASE			"${CMAKE_CXX_FLAGS_RELEASE_INIT}		${FLAGS_RELEASE}")
string(CONCAT CMAKE_CXX_FLAGS_RELWITHDEBINFO	"${CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT}	${FLAGS_RELWITHDEBINFO}")

string(CONCAT CMAKE_C_FLAGS					"${CMAKE_C_FLAGS_INIT}					${COMPILER_FLAGS}")
string(CONCAT CMAKE_C_FLAGS_DEBUG			"${CMAKE_C_FLAGS_DEBUG_INIT}			${FLAGS_DEBUG}")
string(CONCAT CMAKE_C_FLAGS_MINSIZEREL		"${CMAKE_C_FLAGS_MINSIZEREL_INIT}		${FLAGS_MINSIZEREL}")
string(CONCAT CMAKE_C_FLAGS_RELEASE			"${CMAKE_C_FLAGS_RELEASE_INIT}			${FLAGS_RELEASE}")
string(CONCAT CMAKE_C_FLAGS_RELWITHDEBINFO	"${CMAKE_C_FLAGS_RELWITHDEBINFO_INIT}	${FLAGS_RELWITHDEBINFO}")

set(CMAKE_CXX_CREATE_STATIC_LIBRARY	"<CMAKE_AR> rcs <TARGET> <LINK_FLAGS> <OBJECTS>" CACHE STRING "" FORCE)

