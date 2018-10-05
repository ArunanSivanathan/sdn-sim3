//
// Created by Arunan Sivanathan on 26/2/18.
//

#include "controller.h"

Controller::Controller(int ctrloptc, char *ctrloptv[]) {
}

ushort Controller::toController(struct pPcap::packet_meta *p_m, const unsigned char *packet, struct pcap_pkthdr *header) {
    return 0;
}

void Controller::mirroredTraffic(unsigned long pid, int opt, const unsigned char *packet, struct pcap_pkthdr *header) {

}

SwitchBox *Controller::getServiceSwitch() const {
    return mServiceSwitch;
}

void Controller::setServiceSwitch(SwitchBox *serviceSwitch) {
    Controller::mServiceSwitch = serviceSwitch;
}

void Controller::pushInitialRules() {
//    log_info("Initializing default controller");
    struct pPcap::packet_meta *newMeta;

    newMeta = pPcap::createPacketMeta(nullptr, nullptr,0,0,0,(char*)"0.0.0.0",(char*)"0.0.0.0",0,0);
    mServiceSwitch->flowrulePush(0,newMeta,DROP,0);
}

DataLogger *Controller::getMDataLogger() const {
    return mDataLogger;
}

void Controller::setMDataLogger(DataLogger *mDataLogger) {
    Controller::mDataLogger = mDataLogger;
}
