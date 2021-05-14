cmake_minimum_required(VERSION 3.17)
project(fer_nos C)

set(CMAKE_C_STANDARD 11)

include_directories(lab1)

add_executable(playground.pipe playground/pipe.c)
add_executable(playground.named_pipe playground/named_pipe.c)

add_executable(dummy
        lab1/a.h
        lab1/a_car.c
        lab1/a_entry.c
        lab1/a_semaphore.c
        playground/kirk.c
        playground/spock.c
        playground/pipe.c)

add_executable(lab1b lab1/b.h lab1/b_entry.c lab1/b_process.c)
