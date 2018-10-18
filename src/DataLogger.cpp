//
// Created by Arunan Sivanathan on 26/2/18.
//

#include <curses.h>
#include "DataLogger.h"


LogFile::LogFile(const char *filename, bool enable) {
    this->mWriteEnable = enable;

    if (!(this->mWriteEnable)) {
        this->outfile = nullptr;
        return;
    }

    this->outfile = fopen(filename, "w+");;

    if (!this->outfile)
        throw "File cannot be opened";
}

bool LogFile::writeLine(const char *format, ...) {
    if (!(this->mWriteEnable) || this->outfile == nullptr) return false;

    va_list argPtr;
    va_start(argPtr, format);
    vfprintf(this->outfile, format, argPtr);
    va_end(argPtr);
    return true;
}

LogFile::~LogFile() {
    if (!(this->mWriteEnable) || this->outfile == nullptr) return;
    fclose(this->outfile);
}


DataLogger::DataLogger() {
    std::string fname;
    fname = output_log + "log_packets.csv";
    log_packet = new LogFile(fname.c_str(), true);
    log_packet->writeLine("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", "Packet ID", "TIME", "Size", "eth.src", "eth.dst", "IP.src",
                          "IP.dst", "IP.proto", "port.src", "port.dst");

    fname = output_log + "log_flowentries.csv";
    log_flowEntry = new LogFile(fname.c_str(), false);
    log_flowEntry->writeLine("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n",
                             "ID", "eth.src", "eth.dst", "IP.src", "IP.dst", "IP.proto",
                             "port.src", "port.src", "priority", "action", "packets", "bytes");

    fname = output_log + "log_packetevents.csv";
    log_packetevent = new LogFile(fname.c_str(), false);
    log_packetevent->writeLine("%s,%s,%s,%s,%s,%s\n",
                               "No", "Packet Size", "Arrival",
                               "Waiting", "Service In", "Service Out");

    fname = output_log + "log_event_traverse.csv";
    log_event_traverse = new LogFile(fname.c_str(), false);
    log_event_traverse->writeLine("%s,%s,%s\n","TIME","Packet ID","Event Type");

    fname = output_log + "log_packet_actions.csv";
    log_actions = new LogFile(fname.c_str(), false);
    log_actions->writeLine("%s,%s\n","Packet ID","Match_Flow");

    fname = output_log + "log_packet_flowmatch.csv";
    log_flowmatch = new LogFile(fname.c_str(), false);
    log_flowmatch->writeLine("%s,%s\n","Packet ID","Match_Flow");

    fname = output_log + "log_flowusage_packet.csv";
    log_flowCountuse = new LogFile(fname.c_str(), false);
    log_flowCountuse->writeLine("%s,%s:%s,...,...\n","TIME","Flow ID","Packet count");

    fname = output_log + "log_flowusage_data.csv";
    log_flowRateuse = new LogFile(fname.c_str(), false);
    log_flowRateuse->writeLine("%s,%s:%s,...,...\n","TIME","Flow ID","Packet count");

}

DataLogger::~DataLogger() {
    delete log_packet;
    delete log_flowEntry;
    delete log_packetevent;
    delete log_event_traverse;
    delete log_actions;
    delete log_flowmatch;
    delete log_flowCountuse;
    delete log_flowRateuse;

}
