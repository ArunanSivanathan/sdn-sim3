//
// Created by Arunan Sivanathan on 26/2/18.
//

#ifndef SDN_SIM3_CONTROLLER_H
#define SDN_SIM3_CONTROLLER_H


#include "SwitchBox.h"

class SwitchBox;
class DataLogger;

class Controller {
public:


    explicit Controller(int ctrloptc, char *ctrloptv[]);

    virtual SwitchBox *getServiceSwitch() const;

    virtual void setServiceSwitch(SwitchBox *serviceSwitch);

    DataLogger *getMDataLogger() const;

    void setMDataLogger(DataLogger *mDataLogger);

    virtual ushort toController(struct pPcap::packet_meta *p_m, const unsigned char *packet, struct pcap_pkthdr *header);

    virtual void mirroredTraffic(unsigned long pid, int opt, const unsigned char *packet, struct pcap_pkthdr *header);

    virtual void pushInitialRules();

private:
    DataLogger* mDataLogger;
    SwitchBox* mServiceSwitch;

};


#endif //SDN_SIM3_CONTROLLER_H
