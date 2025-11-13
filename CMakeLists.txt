cmake_minimum_required(VERSION 3.10)
project(Infomate LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)

include_directories(${CMAKE_SOURCE_DIR}/rpi-rgb-led-matrix/include)

add_library(matrix STATIC
    rpi-rgb-led-matrix/lib/graphics.cc
    rpi-rgb-led-matrix/lib/bdf-font.cc
)

add_executable(infomate
    src/main.cpp
    src/TerminalCanvas.cpp
)

target_link_libraries(infomate PRIVATE matrix)
