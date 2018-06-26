//
// Created by Arunan Sivanathan on 3/5/18.
//

#include "SimpleStaticRules.h"

void SimpleStaticRules::pushInitialRules() {
    log_info("Initializing SimpleStaticRules controller");
    struct pPcap::packet_meta *newMeta;

    newMeta = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, (char *) "0.0.0.0", (char *) "0.0.0.0", 0, 0);
    getServiceSwitch()->flowrulePush(0, newMeta, DROP, 0);

    //todo:read from json file
    trackFaceTimeAudioCall();


}


void SimpleStaticRules::trackFaceTimeAudioCall() {
    struct pPcap::packet_meta *r;
    // Facetime out
//    26139	2018-05-03 16:58:04	ac:bc:32:d4:6f:2f	00:00:0c:9f:fa:f2	10.248.46.101		16393	3494	STUN	ChannelData TURN Message

    char ip_address[][16]= {"17.120.252.12", "17.120.252.13", "17.125.249.10", "17.125.249.11", "17.154.66.159", "17.253.67.201",
                "17.253.67.202", "17.253.67.204", "17.253.67.205", "17.253.67.208", "23.77.128.53", "23.77.131.226",
                "23.77.151.183", "23.77.153.183"};

    int i;
    for (i = 0;i<14;i++) {
        r = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, (char *) ip_address[i], (char *) "0.0.0.0", 0, 0);
        getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);
        r = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, (char *) "0.0.0.0", (char *) ip_address[i], 0, 0);
        getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);
    }


}