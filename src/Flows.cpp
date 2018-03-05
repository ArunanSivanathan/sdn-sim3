//
// Created by Arunan Sivanathan on 24/2/18.
//

#include "Flows.h"

FlowRule::FlowRule(unsigned int flowid, unsigned int priority, struct pPcap::packet_meta *match, enum ACTION_TYPE action,
                   unsigned int opt) {
    this->flowId = flowid;
    this->priority = priority;
    this->match = match;
    this->action = action;
    this->opt = opt;

    this->rule_previous= nullptr;
    this->rule_next=nullptr;

    this->meterData=0;
    this->meterPacket=0;
    this->mMeterData_milestone=0;
    this->mMeterPacket_milestone=0;
}


void FlowRule::addInTable(FlowRule **header){
    if (*header== nullptr){
        *header = this;
    }
    else{
        FlowRule *cur_f;
        FlowRule *pre_f;
        cur_f = *header;
        pre_f = nullptr;


        while(cur_f!= nullptr && cur_f->priority > this->priority ){
            pre_f = cur_f;
            cur_f=cur_f->rule_next;
        }

        this->rule_next = cur_f;
        this->rule_previous = pre_f;

        if (pre_f == nullptr){
            *header = this;
        }
        else{
            this->rule_previous->rule_next= this;
        }

        if (this->rule_next!= nullptr)
            this->rule_next->rule_previous =this;

    }

}


FlowRule* FlowRule::findMatchingRule(FlowRule *header, struct pPcap::packet_meta *c_meta){
    FlowRule *c_f;
    c_f=header;
    while(c_f != nullptr){
        // debug("Comparing rule");
        if (FlowRule::compRule(c_f->match,c_meta)){
            return c_f;
        }
        c_f=c_f->rule_next;
    }
    return nullptr;
}


u_short FlowRule::compRule(struct pPcap::packet_meta *m_rule, struct pPcap::packet_meta *m_packet){

    if( m_rule->ether_dhost!=NULL && pPcap::compMac(m_rule->ether_dhost,m_packet->ether_dhost)==0)
    {
        //debug("dhost rule mismatch");
        return 0;
    }

    if( m_rule->ether_shost!=NULL && pPcap::compMac(m_rule->ether_shost,m_packet->ether_shost)==0)
    {
        //debug("shost rule mismatch");
        return 0;
    }
    if( m_rule->ether_type !=0 && m_rule->ether_type != m_packet->ether_type)
    {
        //debug("ether_type rule mismatch");
        return 0;
    }
    /* For future development
        if( m_rule->ip_tos !=0 && m_rule->ip_tos != m_packet->ip_tos)
            return 0;
    */
    if( m_rule->ip_p !=0 && m_rule->ip_p!= m_packet->ip_p)
    {
        //debug("Protocol mismatch");
        return 0;
    }

    if( m_rule->ip_src.s_addr !=0 && m_rule->ip_src.s_addr != m_packet->ip_src.s_addr)
    {
        //debug("src address mismatch");
        return 0;
    }

    if( m_rule->ip_dst.s_addr !=0 && m_rule->ip_dst.s_addr != m_packet->ip_dst.s_addr)
    {
        //debug("dst address mismatch");
        return 0;
    }

    if( m_rule->sport !=0 && m_rule->sport != m_packet->sport)
    {
        //debug("sport mismatch");
        return 0;
    }

    if( m_rule->dport !=0 && m_rule->dport != m_packet->dport)
    {
        //debug("dport mismatch");
        return 0;
    }

    return 1;
}


void FlowRule::setMileStone() {
    mMeterPacket_milestone = meterPacket;
    mMeterData_milestone = meterData;
}

FlowRule::~FlowRule() {
    delete match->ether_dhost;
    delete match->ether_shost;
    delete match;
}
