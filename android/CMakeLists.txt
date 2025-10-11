cmake_minimum_required(VERSION 3.10)
project(CompileHellNative)

set(CMAKE_CXX_STANDARD 17)

add_library( # Sets the name of the library.
    compilehell
    SHARED
    ../engine_src/compilehell.c
    main.cpp
)

# If you have a prebuilt libpython, you can add it as IMPORTED library:
# add_library(python3 SHARED IMPORTED)
# set_target_properties(python3 PROPERTIES IMPORTED_LOCATION ${CMAKE_SOURCE_DIR}/../libs/arm64-v8a/libpython3.11.so)

find_library( log-lib log )
find_library( android-lib android )

target_link_libraries( compilehell
    ${log-lib}
    ${android-lib}
    # python3  # link to libpython if available
)
