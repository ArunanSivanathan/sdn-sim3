//
// Created by Arunan Sivanathan on 1/3/18.
//

#ifndef SDN_SIM3_OF_DEV_CLASSIFIER_H
#define SDN_SIM3_OF_DEV_CLASSIFIER_H


#include <controller.h>

#include <vector>
#include <fstream>

class DeviceClassify: public Controller{
public:
    typedef std::vector<std::string> char_vec_t;

    DeviceClassify(int ctrloptc, char **ctrloptv);

    SwitchBox *getServiceSwitch() const override {
        return Controller::getServiceSwitch();
    }

    void pushInitialRules() override;

    ushort
    toController(struct pPcap::packet_meta *p_m, const unsigned char *packet, struct pcap_pkthdr *header) override;

    void mirroredTraffic(int opt, const unsigned char *packet, struct pcap_pkthdr *header) override;
    int readMacList(const char *filePath, char_vec_t *macList);
    void initiateDeviceIdentificationRules(const char* deviceMac,const char* gatewayMac);
};


#endif //SDN_SIM3_OF_DEV_CLASSIFIER_H
