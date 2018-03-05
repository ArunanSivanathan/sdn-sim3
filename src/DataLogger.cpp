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
    log_packet = new LogFile("./log_packets.csv", false);
    log_packet->writeLine("%s,%s,%s,%s,%s,%s,%s,%s,%s\n", "Packet ID", "TIME", "Size", "eth.src", "eth.dst", "IP.src",
                          "IP.dst", "IP.proto", "port.src", "port.dst");

    log_flowEntry = new LogFile("./log_flowentries.csv", true);
    log_flowEntry->writeLine("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n",
                             "ID", "eth.src", "eth.dst", "IP.src", "IP.dst", "IP.proto",
                             "port.src", "port.src", "priority", "action", "packets", "bytes");

    log_packetevent = new LogFile("./log_packetevents.csv", false);
    log_packetevent->writeLine("%s,%s,%s,%s,%s,%s\n",
                               "No", "Packet Size", "Arrival",
                               "Waiting", "Service In", "Service Out");

    log_event_traverse = new LogFile("./log_event_traverse.csv", false);
    log_event_traverse->writeLine("%s,%s,%s\n","TIME","Packet ID","Event Type");

    log_actions = new LogFile("./log_packet_actions.csv", true);
    log_actions->writeLine("%s,%s,%s,%s\n","TIME","Packet ID","Packet Size","Match_Flow");

    log_flowmatch = new LogFile("./log_packet_flowmatch.csv", true);
    log_flowmatch->writeLine("%s,%s,%s,%s\n","TIME","Packet ID","Packet Size","Match_Flow");

    log_flowCountuse = new LogFile("./log_flowusage_packet.csv", true);
    log_flowCountuse->writeLine("%s,%s:%s,...,...\n","TIME","Flow ID","Packet count");

    log_flowRateuse = new LogFile("./log_flowusage_data.csv", true);
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
