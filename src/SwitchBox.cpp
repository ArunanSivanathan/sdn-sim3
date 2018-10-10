//
// Created by Arunan Sivanathan on 23/2/18.
//


#include "SwitchBox.h"

class DataLogger;

class Controller;

SwitchBox::SwitchBox(Controller *ctrl, DataLogger *dLogger, SimClock *sysClock) {
    this->first_rule = nullptr;
    this->mPacketCount = 0;
    this->mDataCount = 0;
    this->mPacketDropped = 0;
    this->mPacketFWD = 0;
    this->mPacketFWD2ctrl = 0;
    this->mPacketMirrored = 0;
    this->mFlowRuleCount = 0;
    this->mController = ctrl;
    this->mController->setServiceSwitch(this);
    this->mSysClock = sysClock;
    this->mDataLogger = dLogger;

}

void SwitchBox::packetIn(pPcap::sim_pack *new_packet) {
    FlowRule *fMatch;
    pPcap::packet_meta *c_m;


    mSysClock->setCurrentTime(&(new_packet->header->ts));

    c_m = pPcap::getPacketMeta(new_packet); //This will parse upto level 4 and update new_packet as well

    if (c_m == nullptr) goto error;

    if (mDataLogger->log_packet->mWriteEnable) log_packet(new_packet, c_m);




    fMatch = FlowRule::findMatchingRule(this->first_rule, c_m);

    if (takeaction(fMatch, c_m, new_packet)) {
        fMatch = FlowRule::findMatchingRule(this->first_rule, c_m);
        takeaction(fMatch, c_m, new_packet);
    }
    delete c_m;

//    srcMac = pPcap::mac2str( c_m->ether_shost);
//    debug("Src mac %s",srcMac);
//    delete srcMac;

    return;

    error:
    delete c_m;
    return;

}

void SwitchBox::log_packet(const pPcap::sim_pack *new_packet, const pPcap::packet_meta *c_m) const {
    char *srcMac, *dstMac, *srcIP, *dstIP;

    srcMac = pPcap::mac2str(c_m->ether_shost);
    dstMac = pPcap::mac2str(c_m->ether_dhost);
    srcIP = pPcap::ip2str(c_m->ip_src);
    dstIP = pPcap::ip2str(c_m->ip_dst); //todo: need an optimum way to write this
    mDataLogger->log_packet->writeLine("%lu,%lu,%d,%s,%s,%s,%s,%d,%d,%d\n",
                                       new_packet->packet_id,
                                       (long)new_packet->header->ts.tv_sec,
                                       new_packet->header->caplen,
                                       srcMac,
                                       dstMac,
                                       srcIP,
                                       dstIP, c_m->ip_p, c_m->sport, c_m->dport);


    free(srcMac);
    free(dstMac);
    free(srcIP);
    free(dstIP);
}

FlowRule *SwitchBox::flowrulePush(unsigned int priority, struct pPcap::packet_meta *match,
                                  enum ACTION_TYPE action, unsigned int opt) {

    static unsigned int fcounter = 0;

    FlowRule *newRule = new FlowRule(fcounter++, priority, match, action, opt);

    newRule->addInTable(&(this->first_rule));
    mFlowRuleCount++;
    return newRule;
}


ushort
SwitchBox::takeaction(FlowRule *c_f, struct pPcap::packet_meta *c_meta, pPcap::sim_pack *new_packet) {

    this->mPacketCount += 1;
    this->mDataCount += new_packet->header->caplen;


    if (c_f == nullptr) {//No matching rule
//      debug("%lu:\tPacket send to controller",pid);
        ushort reMatch = this->mController->toController(new_packet, c_meta);
        this->mPacketFWD2ctrl += 1;
        return reMatch;
    } else {
        c_f->meterPacket += 1;//Increase packet counter
        c_f->meterData += new_packet->header->caplen;//Increase data counter
    }

//    if (!(c_f->action & FWD_TO_CONTROLLER)) print_packet_action(pid,c_f->action,header);//To avoid

//    char *timestr = SimClockTime(&(new_packet->header->ts)).getFormattedTime("%Y-%m-%d %H:%M:%S");

    mDataLogger->log_actions->writeLine("%lu,%d\n", new_packet->packet_id, c_f->action);
    mDataLogger->log_flowmatch->writeLine("%lu,%d\n", new_packet->packet_id, c_f->flowId);
//    delete timestr;

    if (~(c_f->action) & DROP) {
        //debug("%lu:\tPacket Forwarded",pid);
        this->mPacketFWD += 1;
    }
    if (c_f->action & DROP) {
        //debug("%lu:\tPacket Dropped",pid);
        this->mPacketDropped += 1;
    }
    if (c_f->action & FWD_TO_CONTROLLER) {
        //debug("%lu:\tPacket fwd to controller",pid);
        ushort reMatch = this->mController->toController(new_packet, c_meta);
        this->mPacketFWD2ctrl += 1;
        return reMatch;//Rematch the packets
    }
    if (c_f->action & MIRROR_TRAFFIC) {
        //debug("%lu:\tPacket fwd to deep_analysis",pid);
        this->mController->mirroredTraffic(new_packet, c_f->opt);
        this->mPacketMirrored += 1;
        this->mPacketFWD += 1;
        return 0;//Rematch the packets
    }
    return 0;
}

void SwitchBox::logFlowActivity(long upTime) {
    FlowRule *c_f;
    unsigned long flowUse;

    mDataLogger->log_flowCountuse->writeLine("%d", upTime);
    mDataLogger->log_flowRateuse->writeLine("%d", upTime);

    c_f = this->first_rule;
    while (c_f != nullptr) {
        flowUse = c_f->meterData - c_f->mMeterData_milestone;
        if (flowUse != 0) mDataLogger->log_flowRateuse->writeLine(",%d:%llu", c_f->flowId, flowUse);

        flowUse = c_f->meterPacket - c_f->mMeterPacket_milestone;
        if (flowUse != 0) mDataLogger->log_flowCountuse->writeLine(",%d:%llu", c_f->flowId, flowUse);

        c_f->setMileStone();
        c_f = c_f->rule_next;
    }
    mDataLogger->log_flowCountuse->writeLine("\n");
    mDataLogger->log_flowRateuse->writeLine("\n");
}

void SwitchBox::logFlowInformations() {
    struct FlowRule *c_f;
    char *srcMac, *dstMac, *srcIP, *dstIP;

    //int i=0;
    c_f = this->first_rule;

    while (c_f != NULL) {
        srcMac = pPcap::mac2str(c_f->match->ether_shost);
        dstMac = pPcap::mac2str(c_f->match->ether_dhost);
        srcIP = pPcap::ip2str(c_f->match->ip_src);
        dstIP = pPcap::ip2str(c_f->match->ip_dst);

        mDataLogger->log_flowEntry->writeLine("%04d,%s,%s,%s,%s,0x%x,%d,%d,%d,%d,%lu,%lu\n",
                                              c_f->flowId,
                                              srcMac,
                                              dstMac,
                                              srcIP,
                                              dstIP,
                                              c_f->match->ip_p,
                                              c_f->match->sport,
                                              c_f->match->dport,

                                              c_f->priority,
                                              c_f->action,
                                              c_f->meterPacket,
                                              c_f->meterData);

        delete (srcMac);
        delete (dstMac);
        delete (srcIP);
        delete (dstIP);
        c_f = c_f->rule_next;
    }
}

void SwitchBox::logSummary() {
    fprintf(stdout, "\nSummary\n");
    fprintf(stdout, "Total no of packets:\t%lu\n", mPacketCount);
    fprintf(stdout, "Total data :\t%lu Bytes\n", mDataCount);
    fprintf(stdout, "No of drop:\t%lu\n", mPacketDropped);
    fprintf(stdout, "No of forwards:\t%lu\n", mPacketFWD);
    fprintf(stdout, "No of forwards to controller:\t%lu\n", mPacketFWD2ctrl);
    fprintf(stdout, "No of mirrored:\t%lu\n", mPacketMirrored);
    fprintf(stdout, "Total flowrules:\t%d\n", mFlowRuleCount);
}

SwitchBox::~SwitchBox() {
    FlowRule *c_f;
    FlowRule *p_f;

    //Flush all flowlog by ticking the timer to next frame
    if (FLUSH_END_LAST_SECONDS == true)
        logFlowActivity(mSysClock->getUpTime() + 1);
    logFlowInformations();
    logSummary();

    //Delete all flows
    c_f = this->first_rule;
    while (c_f != nullptr) {
        p_f = c_f;
        c_f = c_f->rule_next;
        delete (p_f);
    }

}

