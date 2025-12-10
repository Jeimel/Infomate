cmake_minimum_required(VERSION 3.16)
project(Infomate VERSION 1.0.0 LANGUAGES CXX)

option(USE_RGB_MATRIX "Build with RGB Matrix support (requires Raspberry Pi)" OFF)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(EXTERNAL_DIR ${CMAKE_SOURCE_DIR}/external)

# =============================================================================
# asio
# =============================================================================

add_library(asio INTERFACE)

target_include_directories(asio INTERFACE ${EXTERNAL_DIR}/asio/include)
target_compile_definitions(asio INTERFACE ASIO_STANDALONE)

# =============================================================================
# crow
# =============================================================================

add_library(crow INTERFACE)

target_include_directories(crow INTERFACE  ${EXTERNAL_DIR}/crow/include)
target_link_libraries(crow INTERFACE asio)

# =============================================================================
# rpi-rgb-led-matrix
# =============================================================================

set(MATRIX_DIR ${EXTERNAL_DIR}/rpi-rgb-led-matrix)

add_library(matrix STATIC
    ${MATRIX_DIR}/lib/graphics.cc
    ${MATRIX_DIR}/lib/bdf-font.cc
)

target_include_directories(matrix PUBLIC ${MATRIX_DIR}/include)

# =============================================================================
# rpi-rgb-led-matrix (hardware)
# =============================================================================

if(USE_RGB_MATRIX)
    add_custom_command(
        OUTPUT ${MATRIX_DIR}/lib/librgbmatrix.a
        COMMAND make -C ${MATRIX_DIR}/lib
        WORKING_DIRECTORY ${MATRIX_DIR}
    )

    add_custom_target(rgbmatrix_build 
        DEPENDS ${MATRIX_DIR}/lib/librgbmatrix.a
    )

    add_library(rgbmatrix STATIC IMPORTED GLOBAL)
    set_target_properties(rgbmatrix PROPERTIES
        IMPORTED_LOCATION ${MATRIX_DIR}/lib/librgbmatrix.a
        INTERFACE_INCLUDE_DIRECTORIES ${MATRIX_DIR}/include
    )
    add_dependencies(rgbmatrix rgbmatrix_build)
endif()

# =============================================================================
# Apps
# =============================================================================

file(GLOB APP_HEADERS ${CMAKE_SOURCE_DIR}/apps/*/*.h)

file(WRITE ${CMAKE_BINARY_DIR}/apps.h "")

foreach(header ${APP_HEADERS})
    file(APPEND ${CMAKE_BINARY_DIR}/apps.h "#include \"${header}\"\n")
endforeach()

# =============================================================================
# Infomate
# =============================================================================

set(SOURCES
    src/main.cpp
    src/manager.cpp
    src/adapter/terminal.h
    src/adapter/api.h
)

set(HEADERS
    include/app.h
    include/display.h
    include/input.h
    include/manager.h
    include/registry.h
)

add_executable(${PROJECT_NAME} ${SOURCES} ${HEADERS})

target_include_directories(${PROJECT_NAME} PRIVATE
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_BINARY_DIR}
)

target_link_libraries(${PROJECT_NAME} PRIVATE 
    crow
    matrix
)

if(USE_RGB_MATRIX)
    target_compile_definitions(${PROJECT_NAME} PRIVATE USE_RGB_MATRIX)
    target_link_libraries(${PROJECT_NAME} PRIVATE rgbmatrix)
    list(APPEND HEADERS adapter/matrix.h)
endif()

target_compile_definitions(${PROJECT_NAME} PRIVATE
    INFOMATE_VERSION="${PROJECT_VERSION}"
    FONT_DIR="${MATRIX_DIR}/fonts"
)
