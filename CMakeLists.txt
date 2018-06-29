cmake_minimum_required(VERSION 3.8)
project(sdn_sim3)

set(CMAKE_CXX_STANDARD 11)

SET(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/")
include_directories ("${PROJECT_SOURCE_DIR}/include")


set(HEADER_FILES include/SwitchBox.h src/pcapParser.cpp include/pcapParser.h src/logistics.cpp include/logistics.h include/Flows.h include/config.h include/controller.h include/DataLogger.h include/SimClock.h include/main.h)
set(SOURCE_FILES main.cpp src/SwitchBox.cpp src/pcapParser.cpp src/logistics.cpp src/Flows.cpp src/controller.cpp src/DataLogger.cpp src/SimClock.cpp)
set(APPS apps/DeviceClassify.cpp apps/DeviceClassify.h apps/apps.cpp apps/apps.h apps/SimpleStaticRules.cpp apps/SimpleStaticRules.h)

add_executable(sdn_sim3 ${SOURCE_FILES} ${HEADER_FILES} ${APPS})

include(FindPCAP.cmake)
target_link_libraries(sdn_sim3 ${PCAP_LIBRARY})