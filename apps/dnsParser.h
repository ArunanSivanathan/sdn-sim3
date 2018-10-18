//
// Created by Arunan Sivanathan on 28/9/18.
//

#ifndef SDN_SIM3_DNSPARSER_H
#define SDN_SIM3_DNSPARSER_H

#include <controller.h>

#include <vector>
#include <fstream>
#include <cstring>
#include <stdexcept>
#include <stdio.h>

#include "IPaddress.h"
#include "DataLogger.h"
#include "config.h"

#define DNS_HEADER_SIZE 12

#define T_IPv4 1 //Ipv4 address
#define T_IPv6 28 //Ipv4 address
#define T_NS 2 //Nameserver
#define T_CNAME 5 // canonical name
#define T_SOA 6 /* start of authority zone */
#define T_PTR 12 /* domain name pointer */
#define T_MX 15 //Mail server

#define MOVE_PAYLOAD_POINTER(_PAYLOAD, _LEN, _SIZE) {               \
    _PAYLOAD += _SIZE; \
    _LEN -= _SIZE;}






extern std::string output_log;
#define DEBUG_PAYLOAD(msg,payload,len){ fprintf(stdout,"%s: ",msg); for (int i = 0; i < len; i++) { \
fprintf(stdout, "%02x\t", *(payload +i));}fprintf(stdout, "\n");}

struct DNS_HEADER_FLAGS {
#if __DARWIN_BYTE_ORDER == __DARWIN_LITTLE_ENDIAN
    unsigned char rd :1; // recursion desired
    unsigned char tc :1; // truncated message
    unsigned char aa :1; // authoritive answer
    unsigned char opcode :4; // purpose of message
    unsigned char qr :1; // query/response flag

    unsigned char rcode :4; // response code
    unsigned char cd :1; // checking disabled
    unsigned char ad :1; // authenticated data
    unsigned char z :1; // its z! reserved
    unsigned char ra :1; // recursion available

#endif
#if __DARWIN_BYTE_ORDER == __DARWIN_BIG_ENDIAN
    unsigned char qr :1; // query/response flag
    unsigned char opcode :4; // purpose of message
    unsigned char aa :1; // authoritive answer
    unsigned char tc :1; // truncated message
    unsigned char rd :1; // recursion desired

    unsigned char ra :1; // recursion available
    unsigned char z :1; // its z! reserved
    unsigned char ad :1; // authenticated data
    unsigned char cd :1; // checking disabled
    unsigned char rcode :4; // response code
#endif
};

//Constant sized fields of query structure
struct QUESTION {
    unsigned short qtype;
    unsigned short qclass;
};

//Structure of a Query
struct QUERY{
    std::string name;
    struct QUESTION question;
} ;

//Constant sized fields of the resource record structure
#pragma pack(push, 1)
struct R_DATA {
    unsigned short type;
    unsigned short _class;
    unsigned int ttl;
    unsigned short data_len;
};
#pragma pack(pop)

//Pointers to resource record contents
struct RES_RECORD {
    std::string name;
    struct R_DATA resource;
    std::string rdata;
};



//DNS header structure
class DNSPayload{

public:

private:
    uint32_t readQueries(const unsigned char *payload, uint32_t payload_len, uint32_t *gbl_payload_pointer);
    uint32_t readRes(vector<RES_RECORD> *output_vect, unsigned short count, const unsigned char *payload,
                     uint32_t payload_len, uint32_t *gbl_payload_pointer);

    uint32_t readDomain(char *buff, const unsigned char *payload, uint32_t payload_len, uint32_t *gbl_payload_pointer);

public:
    DNSPayload(const unsigned char *payload,uint32_t payload_len);

    unsigned short m_transid; // identification number
    struct DNS_HEADER_FLAGS *m_flags;
    unsigned short m_count_quries; // number of question entries
    unsigned short m_count_ans; // number of answer entries
    unsigned short m_count_auth; // number of authority entries
    unsigned short m_count_rec; // number of resource entries

    vector<QUERY> m_v_questions;
    vector<RES_RECORD> m_v_answers;
    vector<RES_RECORD> m_v_authNS;
    vector<RES_RECORD> m_v_addRecs;
};



class DNSParser : public Controller {
    LogFile* dns_rev_resolve_log;
    LogFile* dns_qry_log;
public:
    virtual ~DNSParser();

public:
    typedef std::vector<std::string> char_vec_t;

    DNSParser(int ctrloptc, char **ctrloptv);

    SwitchBox *getServiceSwitch() const override {
        return Controller::getServiceSwitch();
    }

    void pushInitialRules() override;

    ushort
    toController(pPcap::sim_pack *new_packet, struct pPcap::packet_meta *p_m) override;

    void mirroredTraffic(pPcap::sim_pack *new_packet, int opt) override;

    void parse(pPcap::sim_pack *new_packet);
};

#endif //SDN_SIM3_DNSPARSER_H
