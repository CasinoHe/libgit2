import os
import sys
import subprocess


def build_win64(cmake_options=None):
    # Define the parent directory and build directory
    parent_dir = ".."
    build_dir = os.path.join(parent_dir, "build")

    # Create the build directory if it doesn't exist
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)

    # Change the current working directory
    os.chdir(build_dir)

    # Run cmake and make commands
    command = build_cmake_parameters(parent_dir, cmake_options)
    subprocess.call(command)
    subprocess.call(["make", "--build", "."])


def build_cmake_parameters(parent_dir, cmake_options=None):
    # Start with the base command
    command = ["cmake", parent_dir]

    # If there are additional options, add them to the command
    if cmake_options:
        for option, value in cmake_options.items():
            command.append(f"-D{option}={value}")

    return command


def check_unreal_engine(path):
    # Check if the path is valid
    if not os.path.exists(path):
        print(f"Invalid Unreal Engine path: {path}")
        return False

    # Check if the path contains the Engine/Source directory
    if not os.path.exists(os.path.join(path, "Engine", "Source")):
        print(f"Invalid Unreal Engine path: {path}")
        return False

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_win64.py [Unreal Engine Path]")
        exit()

    # check the unreal engine path
    unreal_path = sys.argv[1]
    if not check_unreal_engine(unreal_path):
        exit()

    cmake_options = {"CMAKE_BUILD_TYPE": "Release",
                     "CMAKE_EXPORT_COMPILE_COMMANDS": "1",
                     "BUILD_SHARED_LIBS": "OFF",
                     "BUILD_TESTS": "OFF",
                     "BUILD_CLI": "OFF",
                     "OPENSSL_ROOT_DIR": f"{unreal_path}/Engine/Source/ThirdParty/OpenSSL/1.1.1t",
                     "OPENSSL_INCLUDE_DIR": f"{unreal_path}/Engine/Source/ThirdParty/OpenSSL/1.1.1t/include/Win64/VS2015/openssl",
                     "OPENSSL_LIBRARIES": f"{unreal_path}/Engine/Source/ThirdParty/OpenSSL/1.1.1t/lib/Win64/VS2015/Release",
                     }

    # Example usage:
    build_win64(cmake_options)
