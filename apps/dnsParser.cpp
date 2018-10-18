//
// Created by Arunan Sivanathan on 28/9/18.
// --verbose -r 60 "/Users/Arunan/Documents/PCAP-Transfer/States/17-09-26.pcap" pcapparser
//

#include "dnsParser.h"


DNSParser::DNSParser(int ctrloptc, char **ctrloptv) : Controller(ctrloptc, ctrloptv) {
    std::string ip_resolver_filename = output_log + "log_dns.csv";
    this->dns_rev_resolve_log = new LogFile(ip_resolver_filename.c_str(), true);
    this->dns_rev_resolve_log->writeLine("%s,%s,%s\n", "Packet ID", "name", "rdata");

    std::string dns_quries_filename = output_log + "log_dns_quries.csv";
    this->dns_qry_log = new LogFile(dns_quries_filename.c_str(), true);
    this->dns_qry_log->writeLine("%s,%s\n", "Packet ID", "query");
}

DNSParser::~DNSParser() {
    delete this->dns_rev_resolve_log;
    delete this->dns_qry_log;
}

void DNSParser::pushInitialRules() {
    log_info("Initializing DNSParser controller");
    Controller::pushInitialRules();
    //todo: push port 53 packets to mirror
    struct pPcap::packet_meta *r;
    // mac->gateway+DNS
    r = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, "0.0.0.0", "0.0.0.0", 0, 53);
    getServiceSwitch()->flowrulePush(1 << 4, r, MIRROR_TRAFFIC, 0);

    r = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, "0.0.0.0", "0.0.0.0", 53, 0);
    getServiceSwitch()->flowrulePush(1 << 4, r, MIRROR_TRAFFIC, 0);
    verbose("Port 53 is mirrored to DNS parser");
}

ushort
DNSParser::toController(pPcap::sim_pack *new_packet, struct pPcap::packet_meta *p_m) {
    return Controller::toController(new_packet, p_m);
}

void DNSParser::mirroredTraffic(pPcap::sim_pack *new_packet, int opt) {
    Controller::mirroredTraffic(nullptr, opt);

//     to debug packet headers
//    pPcap::packet_meta *c_m;
//    c_m = pPcap::getPacketMeta(new_packet);
//    log_info("dns packet: %lu, %d,%d", new_packet->packet_id, c_m->sport, c_m->dport);


    //todo: write packet id, domain name and IP
    parse(new_packet);
}

void DNSParser::parse(pPcap::sim_pack *new_packet) {
    DNSPayload *dns_payload= nullptr;
    uint32_t payload_len;
    const unsigned char *payload;

    pPcap::l2_head *l2Head = nullptr;
    pPcap::l3_head *l3Head = nullptr;
    pPcap::l4_head *l4Head = nullptr;

    l2Head = pPcap::getLayer2(new_packet->packet, new_packet->header->caplen);
    if (l2Head == nullptr) {
        //      log_warn("layer2 returned null");
        goto error;
    }

    l3Head = pPcap::getLayer3(l2Head);
    if (l3Head == nullptr) {
        //      log_warn("layer3 returned null");
        goto error;
    }

    if (l3Head->ip_p != IPPROTO_UDP) {
        log_err("DNS packet parsing supports only on UDP DNS");
        return;
    }

    l4Head = pPcap::getLayer4(l3Head);
    if (l4Head == nullptr) {
        //      log_warn("layer4 returned null");
        goto error;
    }

    payload = l4Head->payload;
    payload_len = l4Head->payload_len;

    try {
        dns_payload = new DNSPayload(payload, payload_len);
    } catch (pPcap::PacketCorruption& e){
        log_err("DNS parser:%s",e.what());
        delete(dns_payload);
        goto error;
    }

//    for (int i = 0; i < dns_payload->m_v_questions.size(); i++)
//        log_info("DNS Questions Found %s", dns_payload->m_v_questions[i].name.c_str());
//
    if (dns_payload->m_flags->qr == 0){
        for (int i = 0; i < dns_payload->m_v_questions.size(); i++) {

            this->dns_qry_log->writeLine("%lu,%s\n", new_packet->packet_id,
                                                 dns_payload->m_v_questions[i].name.c_str());
        }
    }

    for (int i = 0; i < dns_payload->m_v_answers.size(); i++) {

        this->dns_rev_resolve_log->writeLine("%lu,%s,%s\n", new_packet->packet_id,
                                             dns_payload->m_v_answers[i].name.c_str(),
                                             dns_payload->m_v_answers[i].rdata.c_str());
   }


    for (int i = 0; i < dns_payload->m_v_authNS.size(); i++) {

        this->dns_rev_resolve_log->writeLine("%lu,%s,%s\n", new_packet->packet_id,
                                             dns_payload->m_v_authNS[i].name.c_str(),
                                             dns_payload->m_v_authNS[i].rdata.c_str());
    }


    for (int i = 0; i < dns_payload->m_v_addRecs.size(); i++) {

        this->dns_rev_resolve_log->writeLine("%lu,%s,%s\n", new_packet->packet_id,
                                             dns_payload->m_v_addRecs[i].name.c_str(),
                                             dns_payload->m_v_addRecs[i].rdata.c_str());
    }
//
//    if (dns_payload->m_v_answers.size() > 1) {
//        exit(EXIT_SUCCESS);
//    }

    delete(dns_payload);
    error:
//    delete(dns_payload);
    delete l2Head;
    delete l3Head;
    delete l4Head;
}


DNSPayload::DNSPayload(const unsigned char *payload, uint32_t payload_len) {
    uint32_t gbl_payload_point = 0;

    if (payload_len - gbl_payload_point < DNS_HEADER_SIZE) {
        throw pPcap::PacketCorruption("DNS header corrupted");
    }

    this->m_transid = ntohs(*((unsigned short *) (payload + gbl_payload_point)));
    gbl_payload_point += sizeof(unsigned short);
//    MOVE_PAYLOAD_POINTER(payload, payload_len, sizeof(unsigned short));
//    log_info("ID:%04x",this->m_transid);



    this->m_flags = (struct DNS_HEADER_FLAGS *) (payload + gbl_payload_point);
    gbl_payload_point += sizeof(struct DNS_HEADER_FLAGS);
//    log_info("qr:%01x",this->m_flags->qr);
//    log_info("opcode:%04x",this->m_flags->opcode);
//    log_info("aa:%01x",this->m_flags->aa);
//    log_info("tc:%01x",this->m_flags->tc);
//    log_info("rd:%01x",this->m_flags->rd);

//    for (int i = 0; i < 10; i++) {
//        fprintf(stderr, "%02x\t", payload[i]);
//    }

    this->m_count_quries = htons(*((unsigned short *) (payload + gbl_payload_point)));
    gbl_payload_point += sizeof(unsigned short);

    this->m_count_ans = ntohs(*((unsigned short *) (payload + gbl_payload_point)));
    gbl_payload_point += sizeof(unsigned short);

    this->m_count_auth = ntohs(*((unsigned short *) (payload + gbl_payload_point)));
    gbl_payload_point += sizeof(unsigned short);

    this->m_count_rec = ntohs(*((unsigned short *) (payload + gbl_payload_point)));
    gbl_payload_point += sizeof(unsigned short);

    /***Read questions***/
    if (this->m_count_quries > 0 && payload_len - gbl_payload_point < 1) {
        throw pPcap::PacketCorruption("DNS quries payload corrupted");
    }
    this->readQueries(payload, payload_len, &gbl_payload_point);

    /***Read answers***/
    if (this->m_count_ans > 0 && payload_len - gbl_payload_point < 1) {
        throw pPcap::PacketCorruption("DNS answers payload corrupted");
    }
    this->readRes(&m_v_answers, m_count_ans, payload, payload_len, &gbl_payload_point);

    /***Read authoritative ns***/
//    log_info("Reading authoritative ns");
//    DEBUG_PAYLOAD(payload+gbl_payload_point,5);
    if (this->m_count_auth > 0 && payload_len - gbl_payload_point < 1) {
        throw pPcap::PacketCorruption("DNS answers payload corrupted");
    }
    this->readRes(&m_v_authNS, m_count_auth, payload, payload_len, &gbl_payload_point);

    /***Read additional records***/
//    log_info("Reading records");
    if (this->m_count_rec > 0 && payload_len - gbl_payload_point < 1) {
        throw pPcap::PacketCorruption("DNS answers payload corrupted");
    }
    this->readRes(&m_v_addRecs, m_count_rec, payload, payload_len, &gbl_payload_point);


}

uint32_t DNSPayload::readQueries(const unsigned char *payload, uint32_t payload_len, uint32_t *gbl_payload_pointer) {
    char buff[255];
    int i_count;
    QUERY qry;


    for (i_count = 0; i_count < this->m_count_quries; i_count++) {

        this->readDomain(buff, payload, payload_len, gbl_payload_pointer);
        qry.name = std::string(buff);

        if (payload_len - *gbl_payload_pointer < sizeof(struct QUESTION)) {
            throw pPcap::PacketCorruption("DNS queries corrupted");
        }

        qry.question.qtype = ntohs(*((unsigned short *) (payload + *gbl_payload_pointer)));
        *gbl_payload_pointer += sizeof(unsigned short);

        qry.question.qclass = ntohs(*((unsigned short *) (payload + *gbl_payload_pointer)));
        *gbl_payload_pointer += sizeof(unsigned short);

        this->m_v_questions.push_back(qry);

    }

    return *gbl_payload_pointer;

}

uint32_t DNSPayload::readRes(vector<RES_RECORD> *output_vect, unsigned short count, const unsigned char *payload,
                             uint32_t payload_len, uint32_t *gbl_payload_pointer) {
    char buff[255];
    int i_count;
    RES_RECORD rec;


    for (i_count = 0; i_count < count; i_count++) {


        this->readDomain(buff, payload, payload_len, gbl_payload_pointer);

        rec.name = std::string(buff);

        if (payload_len - *gbl_payload_pointer < sizeof(struct R_DATA)) {
            throw pPcap::PacketCorruption("DNS rec corrupted in Ans/AuthNS/AddRes");
        }

        rec.resource.type = ntohs(*((unsigned short *) (payload + *gbl_payload_pointer)));
        *gbl_payload_pointer += sizeof(unsigned short);

        rec.resource._class = ntohs(*((unsigned short *) (payload + *gbl_payload_pointer)));
        *gbl_payload_pointer += sizeof(unsigned short);

        rec.resource.ttl = ntohs(*((unsigned int *) (payload + *gbl_payload_pointer)));
        *gbl_payload_pointer += sizeof(unsigned int);


        rec.resource.data_len = ntohs(*((unsigned short *) (payload + *gbl_payload_pointer)));
        *gbl_payload_pointer += sizeof(unsigned short);


        if (payload_len - *gbl_payload_pointer < rec.resource.data_len) {
            throw pPcap::PacketCorruption("DNS resource data corrupted in Ans/AuthNS/AddRes");
        }


        if (rec.resource.type == T_IPv4 && rec.resource.data_len == 4) {//if its an ipv4 address
            IPv4 ipv4_address;
            ipv4_address.fromBytes(payload + *gbl_payload_pointer);
            rec.rdata = ipv4_address.to_string();
            *gbl_payload_pointer += ipv4_address._bytecount;

        } else if (rec.resource.type == T_IPv6 && rec.resource.data_len == 16) {//if its an ipv6 address
            IPv6 ipv6_address;
            ipv6_address.fromBytes(payload + *gbl_payload_pointer);
            rec.rdata = ipv6_address.to_string();
            *gbl_payload_pointer += ipv6_address._bytecount;
        } else {
            uint32_t initial_point = *gbl_payload_pointer;
            this->readDomain(buff, payload, payload_len, gbl_payload_pointer);
            rec.rdata = std::string(buff);

//            if (*gbl_payload_pointer - initial_point != rec.resource.data_len) {
//                throw pPcap::PacketCorruption("DNS resource data length mismatch in Ans/AuthNS/AddRes");
//            }
        }


        output_vect->push_back(rec);

    }

    return *gbl_payload_pointer;

}

uint32_t
DNSPayload::readDomain(char *buff, const unsigned char *payload, uint32_t payload_len, uint32_t *gbl_payload_pointer) {

    unsigned short noChar;
    unsigned short buff_pos = 0;
    uint32_t local_pointer = *gbl_payload_pointer;
    bool on_offset = false;

    //now convert 3www6google3com0 to www.google.com
    while (payload[local_pointer] && local_pointer < payload_len) {//Until find a Null or no more payload
        if (payload[local_pointer] >= 192) {
            //49152 = 11000000 00000000
            local_pointer = (payload[local_pointer]) * 256 + payload[(local_pointer + 1)] - 49152;
            on_offset = true; //we have jumped to another location so counting wont go up!

        } else {
            buff[buff_pos++] = payload[local_pointer++];
            if (!on_offset) {
                (*gbl_payload_pointer)++; //if we haven't jumped to another location then we can count the global pointer
            }
        }
    }
    if (!on_offset)
        (*gbl_payload_pointer) += 1; //If we haven't jumped we have to pass null character
    else
        (*gbl_payload_pointer) += 2; //We have to pass offset bytes


    buff[buff_pos] = '\0';
    unsigned short buff_len = buff_pos;

    //now convert 3www6google3com0 to www.google.com
    for (buff_pos = 0; buff_pos < buff_len; buff_pos++) {
        noChar = (unsigned short) buff[buff_pos];
        for (int i = 0; i < noChar; i++) {
            buff[buff_pos] = buff[buff_pos + 1];
            buff_pos = buff_pos + 1;
        }
        buff[buff_pos] = '.';
    }
    buff[buff_pos - 1] = '\0'; //remove the last dot
    return *gbl_payload_pointer;


}




