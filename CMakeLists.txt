cmake_minimum_required(VERSION 3.10)
project(Infomate LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include_directories(${CMAKE_SOURCE_DIR}/rpi-rgb-led-matrix/include)

include_directories(${CMAKE_SOURCE_DIR}/include)

include_directories(${CMAKE_SOURCE_DIR}/src/apps)

add_library(matrix STATIC
    rpi-rgb-led-matrix/lib/graphics.cc
    rpi-rgb-led-matrix/lib/bdf-font.cc
)

file(GLOB SRC_FILES
    src/*.cpp
    src/app/*.cpp
)

add_executable(infomate ${SRC_FILES})

target_link_libraries(infomate PRIVATE matrix)
