//
// Created by Arunan Sivanathan on 24/2/18.
//

#ifndef SDN_SIM3_CONFIG_H
#define SDN_SIM3_CONFIG_H

#include <fstream>
#define LOG_FLOW_ACTIVITY 1
#define LOG_FLOWS 1
#define LOG_PACKETS 0
#define LOG_EVENTS 0


extern int verboseFlag;
extern int resolution;
extern std::string output_log;
#define FLOW_ACTIVITY_WITH_EPOCH_TIME true
#define FLUSH_END_LAST_SECONDS false

#endif //SDN_SIM3_CONFIG_H
