import argparse

parser = argparse.ArgumentParser(description="Create a new JAPI project.")
parser.add_argument("guid", type=str, help="Name of the JAPI plugin to create.")
parser.add_argument("author", type=str, help="Author(s) of the project.")
parser.add_argument("--description", type=str, default="A JAPI plugin.", help="Description of the project.")

parser.exit_on_error = True

args = parser.parse_args()

print(f"Creating JAPI project: {args.guid}")

# Create project directory
import os
project_dir = args.guid
os.makedirs(project_dir, exist_ok=True)
print(f"Project directory '{project_dir}' created.")

cmake_lists_content = f"""cmake_minimum_required(VERSION 4.0)
project({args.guid} VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_SHARED_LIBRARY_PREFIX "")

add_library({args.guid} SHARED
        src/plugin.cpp
)

target_include_directories({args.guid} PRIVATE
        src
        includes
)

target_link_libraries({args.guid} PRIVATE
        ${{CMAKE_SOURCE_DIR}}/bins/JAPI.dll)
"""

plugin_h_content = """#ifndef JAPI_REWRITE_TESTPLUGIN_PLUGIN_H
#define JAPI_REWRITE_TESTPLUGIN_PLUGIN_H

#define EXPORT extern "C" __declspec(dllexport)

#include <JoJoAPI.h>

EXPORT JAPIModMeta __stdcall GetModMeta();
EXPORT void __stdcall ModInit();

#define JFATAL(fmt, ...) JAPI_LogMessage(JAPI_LOG_LEVEL_FATAL, fmt, ##__VA_ARGS__)
#define JERROR(fmt, ...) JAPI_LogMessage(JAPI_LOG_LEVEL_ERROR, fmt, ##__VA_ARGS__)
#define JDEBUG(fmt, ...) JAPI_LogMessage(JAPI_LOG_LEVEL_DEBUG, fmt, ##__VA_ARGS__)
#define JWARN(fmt, ...) JAPI_LogMessage(JAPI_LOG_LEVEL_WARN, fmt, ##__VA_ARGS__)
#define JINFO(fmt, ...) JAPI_LogMessage(JAPI_LOG_LEVEL_INFO, fmt, ##__VA_ARGS__)

#endif //JAPI_REWRITE_TESTPLUGIN_PLUGIN_H"""

plugin_cpp_content = f"""#include "plugin.h"

#include <JoJoAPI.h>

JAPIModMeta GetModMeta() {{
    static JAPIModMeta meta = {{
        "{args.guid}",
        "{args.author}",
        "{args.guid}",
        "1.0.0",
        "{args.description}"
    }};

    return meta;
}}

void ModInit() {{
    JINFO("{args.guid} initialized!");
}}"""

# Download includes.zip and extract it
import requests
import zipfile

includes_url = "https://github.com/Kapilarny/JAPI/releases/latest/download/includes.zip"
includes_zip_path = os.path.join(project_dir, "includes.zip")

response = requests.get(includes_url)
if response.status_code != 200:
    print(f"Failed to download includes.zip: {response.status_code}")
    exit(1)

with open(includes_zip_path, "wb") as f:
    f.write(response.content)
    print("Downloaded includes.zip")

# Extract includes.zip
with zipfile.ZipFile(includes_zip_path, 'r') as zip_ref:
    zip_ref.extractall(os.path.join(project_dir, "includes"))
    print("Extracted includes.zip")

os.remove(includes_zip_path)
print("Removed includes.zip")

# Download JAPI.dll
japi_dll_url = "https://github.com/Kapilarny/JAPI/releases/latest/download/JAPI.dll"
japi_dll_path = os.path.join(project_dir, "bins", "JAPI.dll")
os.makedirs(os.path.dirname(japi_dll_path), exist_ok=True)

response = requests.get(japi_dll_url)
if response.status_code != 200:
    print(f"Failed to download JAPI.dll: {response.status_code}")
    exit(1)

with open(japi_dll_path, "wb") as f:
    f.write(response.content)
    print("Downloaded JAPI.dll")

# write the files

with open(os.path.join(project_dir, "CMakeLists.txt"), "w") as f:
    f.write(cmake_lists_content)
    print("CMakeLists.txt created.")

src_dir = os.path.join(project_dir, "src")
os.makedirs(src_dir, exist_ok=True)
with open(os.path.join(src_dir, "plugin.h"), "w") as f:
    f.write(plugin_h_content)
    print("src/plugin.h created.")

with open(os.path.join(src_dir, "plugin.cpp"), "w") as f:
    f.write(plugin_cpp_content)
    print("src/plugin.cpp created.")