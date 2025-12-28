cmake_minimum_required(VERSION 4.0)
project(%%{guid}%% VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_SHARED_LIBRARY_PREFIX "")

add_library(%%{guid}%% SHARED
        src/plugin.cpp
)

target_include_directories(%%{guid}%% PRIVATE
        src
        includes
)

target_link_libraries(%%{guid}%% PRIVATE
        ${{CMAKE_SOURCE_DIR}}/bins/JAPI.dll)