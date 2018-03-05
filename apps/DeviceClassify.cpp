//
// Created by Arunan Sivanathan on 1/3/18.
//

#include <iostream>
#include "DeviceClassify.h"


void DeviceClassify::pushInitialRules() {
    log_info("Initializing DeviceClassifying controller");
    struct pPcap::packet_meta *newMeta;

    newMeta = pPcap::createPacketMeta(nullptr, nullptr,0,0,0,(char*)"0.0.0.0",(char*)"0.0.0.0",0,0);
    getServiceSwitch()->flowrulePush(0,newMeta,DROP,0);

    char_vec_t macList;
    macList.reserve(30);
    readMacList("../config/macaddresslist.txt", &macList);
    for (int i =0;i<macList.size();i++){
        debug("Mac %d: %s",i,macList[i].c_str());
        initiateDeviceIdentificationRules(macList[i].c_str(),"14:cc:20:51:33:ea");
    }
}

ushort
DeviceClassify::toController(struct pPcap::packet_meta *p_m, const unsigned char *packet, struct pcap_pkthdr *header) {
    return Controller::toController(p_m, packet, header);
}

void DeviceClassify::mirroredTraffic(int opt, const unsigned char *packet, struct pcap_pkthdr *header) {
    Controller::mirroredTraffic(opt, packet, header);
}


int DeviceClassify::readMacList(const char *filePath, char_vec_t *macList) {

    std::ifstream inFile;
    char line[30];
    std:string macAddress;

    inFile.open(filePath);
    if (!inFile.is_open()) {
        debug("macaddresslist file cannot be opened");
        exit(EXIT_FAILURE);
    }

    while (!inFile.eof()) {
        inFile >> line;
        line[18]='\0';
        macAddress = line;
        std::transform(macAddress.begin(), macAddress.end(), macAddress.begin(), ::tolower);
        macList->push_back(macAddress);
    }
    inFile.close();
    return 0;
}

void DeviceClassify::initiateDeviceIdentificationRules(const char* deviceMac,const char* gatewayMac){
    struct pPcap::packet_meta *r;
    // mac->gateway+DNS
    r =  pPcap::createPacketMeta(deviceMac,gatewayMac,0,0,0,"0.0.0.0","0.0.0.0",0,53);
    getServiceSwitch()->flowrulePush(1<<4,r,FORWARD,0);

    //gateway+dns->mac
    r =  pPcap::createPacketMeta(gatewayMac,deviceMac,0,0,0,"0.0.0.0","0.0.0.0",53,0);
    getServiceSwitch()->flowrulePush(1<<4,r,FORWARD,0);

    // mac->gateway+NTP
    r =  pPcap::createPacketMeta(deviceMac,gatewayMac,0,0,0,"0.0.0.0","0.0.0.0",0,123);
    getServiceSwitch()->flowrulePush(1<<4,r,FORWARD,0);

    //gateway+NTP->mac
    r =  pPcap::createPacketMeta(gatewayMac,deviceMac,0,0,0,"0.0.0.0","0.0.0.0",123,0);
    getServiceSwitch()->flowrulePush(1<<4,r,FORWARD,0);

    // mac->gateway+SSDPUP
    r =  pPcap::createPacketMeta(deviceMac, nullptr,0,0,0,"0.0.0.0","0.0.0.0",0,1900);
    getServiceSwitch()->flowrulePush(1<<4,r,FORWARD,0);

    // mac->gateway+any other traffic
    r =  pPcap::createPacketMeta(deviceMac,gatewayMac,0,0,0,"0.0.0.0","0.0.0.0",0,0);
    getServiceSwitch()->flowrulePush(1<<2,r,FORWARD,0);

    //gateway+UDP->mac
    r =  pPcap::createPacketMeta(gatewayMac,deviceMac,0,0,0,"0.0.0.0","0.0.0.0",0,0);
    getServiceSwitch()->flowrulePush(1<<2,r,FORWARD,0);

    //local->mac
    r =  pPcap::createPacketMeta(nullptr,deviceMac,0,0,0,"0.0.0.0","0.0.0.0",0,0);
    getServiceSwitch()->flowrulePush(1<<1,r,FORWARD,0);

}
