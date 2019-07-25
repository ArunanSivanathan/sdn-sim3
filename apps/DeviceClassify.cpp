//
// Created by Arunan Sivanathan on 1/3/18.
//

#include <iostream>
#include "DeviceClassify.h"


void DeviceClassify::pushInitialRules() {
    log_info("Initializing DeviceClassifying controller");
    struct pPcap::packet_meta *newMeta;

    newMeta = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, (char *) "0.0.0.0", (char *) "0.0.0.0", 0, 0);
    getServiceSwitch()->flowrulePush(0, newMeta, DROP, 0);

    char_vec_t macList;
    macList.reserve(30);
    //todo: allow to pass configuration as path
    readMacList(this->mac_file, &macList);
    for (int i = 0; i < macList.size(); i++) {
        verbose("Mac %d: %s", i, macList[i].c_str());
        initiateDeviceIdentificationRules(macList[i].c_str(), "14:cc:20:51:33:ea");
    }


}

ushort
DeviceClassify::toController(pPcap::sim_pack *new_packet, struct pPcap::packet_meta *p_m) {
    return Controller::toController(new_packet, p_m);
}

void
DeviceClassify::mirroredTraffic(pPcap::sim_pack *new_packet, int opt) {
    Controller::mirroredTraffic(new_packet, opt);
}


int DeviceClassify::readMacList(const char *filePath, char_vec_t *macList) {

    std::ifstream inFile;
    char line[30];
    string macAddress;

    inFile.open(filePath);
    if (!inFile.is_open()) {
        debug("macaddresslist file cannot be opened");
        exit(EXIT_FAILURE);
    }

    while (!inFile.eof()) {
        inFile >> line;
        line[18] = '\0';
        macAddress = line;
        std::transform(macAddress.begin(), macAddress.end(), macAddress.begin(), ::tolower);
        macList->push_back(macAddress);
    }
    inFile.close();
    return 0;
}

void DeviceClassify::initiateDeviceIdentificationRules(const char *deviceMac, const char *gatewayMac) {
    struct pPcap::packet_meta *r;
    // mac->gateway+DNS
    r = pPcap::createPacketMeta(deviceMac, gatewayMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 53);
    getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);

    //gateway+dns->mac
    r = pPcap::createPacketMeta(gatewayMac, deviceMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 53, 0);
    getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);

    // mac->gateway+NTP
    r = pPcap::createPacketMeta(deviceMac, gatewayMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 123);
    getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);

    //gateway+NTP->mac
    r = pPcap::createPacketMeta(gatewayMac, deviceMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 123, 0);
    getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);

    // mac->gateway+SSDPUP
    r = pPcap::createPacketMeta(deviceMac, nullptr, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 1900);
    getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);

    // mac->gateway+any other traffic
    r = pPcap::createPacketMeta(deviceMac, gatewayMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 0);
    getServiceSwitch()->flowrulePush(1 << 2, r, FORWARD, 0);

    //gateway+UDP->mac
    r = pPcap::createPacketMeta(gatewayMac, deviceMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 0);
    getServiceSwitch()->flowrulePush(1 << 2, r, FORWARD, 0);

    //local->mac
    r = pPcap::createPacketMeta(nullptr, deviceMac, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 0);
    getServiceSwitch()->flowrulePush(1 << 1, r, FORWARD, 0);

}

DeviceClassify::DeviceClassify(int ctrloptc, char **ctrloptv) : Controller(ctrloptc, ctrloptv) {
    struct option app_options[] =
            {
                    {"macfile", required_argument, 0, 'm'},
                    {0,         0,                 0, 0}
            };

    int c;
    while (1) {
        int option_index = 0;

        c = getopt_long(ctrloptc, ctrloptv, "e", app_options, &option_index);
        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c) {
            case 0:
                if (app_options[option_index].flag != 0)
                    break;
                printf("option %s", app_options[option_index].name);
                if (optarg)
                    printf(" with arg %s", optarg);
                printf("\n");
                break;
            case 'm':
                mac_file = optarg;
                verbose("Flowenties are being loaded from \"%s\"", mac_file)
                break;
            case '?':
                /* getopt_long already printed an error message. */
                if (optopt == 'r')
                    log_err("Option -%c requires an argument.\n", optopt);
                log_err("Option --macfile requires an argument.\n");
                exit(EXIT_FAILURE);
                break;
            default:
                log_err("Option requires an argument.\n");
                exit(EXIT_FAILURE);
                abort();
        }

    };

}
