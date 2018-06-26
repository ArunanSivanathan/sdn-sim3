//
// Created by Arunan Sivanathan on 23/2/18.
//

#ifndef SDN_SIM3_SWITCH_H
#define SDN_SIM3_SWITCH_H

#include <logistics.h>
#include <pcapParser.h>
#include "Flows.h"
#include "controller.h"
#include "DataLogger.h"
#include "SimClock.h"
#include "config.h"

class DataLogger;
class Controller;

class SwitchBox {
public:
    explicit SwitchBox(Controller *ctrl, DataLogger *dLogger, SimClock *sysClock);

    virtual ~SwitchBox();

    void packetIn(unsigned int  p_no, const unsigned char *packet, struct pcap_pkthdr *header);

    FlowRule *flowrulePush(unsigned int priority, pPcap::packet_meta *newMatch, enum ACTION_TYPE action,
                                  unsigned int opt);

    ushort takeaction(unsigned long pid, FlowRule *c_f, struct pPcap::packet_meta *c_meta,
                      const unsigned char *packet, struct pcap_pkthdr *header);

    FlowRule *first_rule;

    Controller *mController;
    DataLogger *mDataLogger;

    void logFlowActivity(long upTime);
    void logSummary();

private:
    unsigned long mPacketCount;
    unsigned long mDataCount;
    unsigned long mPacketDropped;
    unsigned long mPacketFWD;
    unsigned long mPacketFWD2ctrl;
    unsigned long mPacketMirrored;
    unsigned int mFlowRuleCount;

    SimClock *mSysClock;


    void logFlowInformations();
};


#endif //SDN_SIM3_SWITCH_H
