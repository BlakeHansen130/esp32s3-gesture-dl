# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/dahao/esp/esp-idf/components/bootloader/subproject"
  "/home/dahao/code/new_start/gesture/build/bootloader"
  "/home/dahao/code/new_start/gesture/build/bootloader-prefix"
  "/home/dahao/code/new_start/gesture/build/bootloader-prefix/tmp"
  "/home/dahao/code/new_start/gesture/build/bootloader-prefix/src/bootloader-stamp"
  "/home/dahao/code/new_start/gesture/build/bootloader-prefix/src"
  "/home/dahao/code/new_start/gesture/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/dahao/code/new_start/gesture/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/dahao/code/new_start/gesture/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
