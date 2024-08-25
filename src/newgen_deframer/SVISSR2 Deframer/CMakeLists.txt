cmake_minimum_required (VERSION 3.0.0)

project (SVISSR-Deframer)
file(GLOB_RECURSE SVISSR-Deframer_CPPS src/*.cpp)

add_executable(SVISSR-Deframer ${SVISSR-Deframer_CPPS})

target_include_directories(SVISSR-Deframer PUBLIC src)

target_link_libraries(SVISSR-Deframer PUBLIC m)

find_package(Threads REQUIRED)
target_link_libraries(SVISSR-Deframer PUBLIC Threads::Threads)

install(TARGETS SVISSR-Deframer DESTINATION bin)