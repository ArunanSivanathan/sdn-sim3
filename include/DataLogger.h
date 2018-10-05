//
// Created by Arunan Sivanathan on 26/2/18.
//

#ifndef SDN_SIM3_DATALOGGER_H
#define SDN_SIM3_DATALOGGER_H


#include <cstdio>
#include "config.h"

using namespace std;

class LogFile {
public:
    FILE *outfile;
    bool mWriteEnable;

    explicit LogFile(const char *filename, bool enable);

    bool writeLine(const char *format, ...);

    virtual ~LogFile();
};

class DataLogger {
public:
    LogFile *log_packet;
    LogFile *log_flowEntry;
    LogFile *log_packetevent;
    LogFile *log_event_traverse;
    LogFile *log_actions;
    LogFile *log_flowmatch;
    LogFile *log_flowCountuse;
    LogFile *log_flowRateuse;

    virtual ~DataLogger();

    explicit DataLogger();
};


#endif //SDN_SIM3_DATALOGGER_H
