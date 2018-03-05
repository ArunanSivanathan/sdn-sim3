//
// Created by Arunan Sivanathan on 24/2/18.
//

#ifndef SDN_SIM3_FLOWS_H
#define SDN_SIM3_FLOWS_H


#include "pcapParser.h"

enum ACTION_TYPE {
    FORWARD = (0 << 0),
    DROP = (1 << 0),
    FWD_TO_CONTROLLER = (1 << 1),
    MIRROR_TRAFFIC = (1 << 2)
};

class FlowRule {
public:
    unsigned int flowId;
    unsigned int priority;
    struct pPcap::packet_meta *match;
    enum ACTION_TYPE action;
    unsigned int opt;
    unsigned long meterData;
    unsigned long meterPacket;
    unsigned long mMeterData_milestone;
    unsigned long mMeterPacket_milestone;

    FlowRule *rule_previous;
    FlowRule *rule_next;

    virtual ~FlowRule();

    explicit FlowRule(unsigned int flowid,unsigned int priority, struct pPcap::packet_meta *newMatch,enum ACTION_TYPE action, unsigned int opt);
    void addInTable(FlowRule **header);

    static u_short compRule(struct pPcap::packet_meta *m_rule, struct pPcap::packet_meta *m_packet);
    static FlowRule* findMatchingRule(FlowRule *header, struct pPcap::packet_meta *c_meta);



    void setMileStone();

};



#endif //SDN_SIM3_FLOWS_H
