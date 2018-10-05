//
// Created by Arunan Sivanathan on 23/2/18.
//

#include <pcap.h>
#include <logistics.h>
#include <cstdlib>
#include <pcapParser.h>

#include "pcapParser.h"


char *pPcap::mac2str(u_char *mac) {
    const uint MAC_STR_LENGTH = 17;
    char *macStr = (char *) malloc(sizeof(char) * (MAC_STR_LENGTH + 1));

    if (mac == NULL) {
        macStr[0] = '\0';
        return macStr;
    }

    snprintf(macStr, (MAC_STR_LENGTH + 1), "%02x:%02x:%02x:%02x:%02x:%02x",
             mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

    return macStr;
}

u_char *pPcap::str2mac(const char *macStr) {
    u_char *mac;
    int tmpHexCodes[ETHER_ADDR_LEN];
    char nullChar;
    mac = nullptr;

    //If no MAC address
    if (macStr==nullptr){
        return nullptr;

    }

    int i;

    if (ETHER_ADDR_LEN ==
        sscanf(macStr, "%x:%x:%x:%x:%x:%x%c", &tmpHexCodes[0], &tmpHexCodes[1], &tmpHexCodes[2], &tmpHexCodes[3],
               &tmpHexCodes[4], &tmpHexCodes[5], &nullChar)) {

        mac = (u_char *) malloc(sizeof(u_char) * ETHER_ADDR_LEN);
        check(mac, "Failed to char*");

        /* convert to uint8_t */
        for (i = 0; i < ETHER_ADDR_LEN; i++)
            mac[i] = (u_char) tmpHexCodes[i];

        return mac;
    } else {
        log_err("Invalid MAC");
        goto error;
    }

    error:
    delete mac;
    return nullptr;
}

char *pPcap::ip2str(struct in_addr ip) {
    char *ip_str;
    ip_str = (char *) malloc(sizeof(char) * 16);

    char* ipaddress = inet_ntoa(ip);
    /* convert to uint8_t */
    int i;

    for (i = 0; i < 16; i++)
        ip_str[i] = (u_char) ipaddress[i];

    return ip_str;
}

struct in_addr pPcap::str2ip(const char *ipStr) {
    struct in_addr ip;

    inet_aton(ipStr, &ip);
    return ip;
}

void pPcap::runParser(char *pcapFile, void (*onNewPacket)(int, const unsigned char *, struct pcap_pkthdr *)) {
    sim_pack new_packet;
    const unsigned char *packet;
    struct pcap_pkthdr header;
    int packetNo;

    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *pcap;
    pcap = pcap_open_offline(pcapFile, errbuf);
    if (pcap == NULL) {
        log_err("error reading pcap file: %s", errbuf);
        goto error;
    }


    packetNo = 1;
    packet = pcap_next(pcap, &header);

    while (packet) {// until packet variable gets NULL

        (*onNewPacket)(packetNo, packet, &header);
        packetNo++;
        packet = pcap_next(pcap, &header);

    }

    return;

    error:
    exit(1);
    return;
}

struct pPcap::l2_head *pPcap::getLayer2(const unsigned char *packet, uint32_t packetSize) {
    struct pPcap::l2_head *l2Head = nullptr;
    l2Head = (struct pPcap::l2_head *) malloc(sizeof(struct pPcap::l2_head));
    check(l2Head, "layer 2 header memory allocation failed");

    if (packetSize < sizeof(struct ether_header)) {
        /* Ethernet header corrupted*/
        log_warn("Corrupted ethernet packet header");
        goto error;
    }

    struct ether_header *eptr;  /* net/ethernet.h */

    /* start with the ether header... */
    eptr = (struct ether_header *) packet;
    l2Head->ether_dhost = eptr->ether_dhost;
    l2Head->ether_shost = eptr->ether_shost;
    l2Head->ether_type = eptr->ether_type;

    /* Skip over the Ethernet header. */
    l2Head->payload = packet + sizeof(struct ether_header);
    l2Head->payload_len = packetSize - sizeof(struct ether_header);


    return l2Head;

    error:
    delete l2Head;
    return nullptr;
}

struct pPcap::l3_head *pPcap::getLayer3(pPcap::l2_head *l2Head) {
    struct ip *p_ip = nullptr;
    unsigned int ipHeaderLen;

    struct pPcap::l3_head *l3Head = nullptr;
    l3Head = (struct pPcap::l3_head *) malloc(sizeof(struct pPcap::l3_head));
    check(l2Head, "layer 3 header memory allocation failed");

    //skip all packets except IPv4
    if (l2Head->ether_type != 0x08) {
//        log_warn("Not an IPV4 packet");
        goto error;
    }
    if (l2Head->payload_len < sizeof(struct ip)) {
        /* IP header corrupted*/
        log_err("IP header corrupted");
        goto error;
    }

    p_ip = (struct ip *) l2Head->payload;

    ipHeaderLen = p_ip->ip_hl * 4;    /* ip_hl is in 4-byte words */
    if (l2Head->payload_len < ipHeaderLen) {
        /* didn't capture the full IP header including options */
        log_err("IP header options not captured in the packet");
        goto error;
    }

    l3Head->ip_tos = p_ip->ip_tos;
    l3Head->ip_p = p_ip->ip_p;
    l3Head->ip_src = p_ip->ip_src;
    l3Head->ip_dst = p_ip->ip_dst;


    /* Skip over the IP header to get to the UDP header. */
    l3Head->payload = l2Head->payload + ipHeaderLen;
    l3Head->payload_len = l2Head->payload_len - ipHeaderLen;

    return l3Head;

    error:
    delete l3Head;
    return nullptr;
}

struct pPcap::l4_head *pPcap::getLayer4(pPcap::l3_head *l3Head) {
    struct pPcap::l4_head *l4Head = nullptr;
    l4Head = (struct pPcap::l4_head *) malloc(sizeof(struct pPcap::l4_head));
    check(l4Head, "layer 4 header memory allocation failed");

    if (l3Head->ip_p == IPPROTO_TCP) {
        if (l3Head->payload_len < sizeof(struct tcphdr)) {
            log_err("TCP header Corrupted");
            goto error;
        }

        struct tcphdr *p_tcp;
        p_tcp = (struct tcphdr *) l3Head->payload;
        l4Head->sport = ntohs(p_tcp->th_sport);
        l4Head->dport = ntohs(p_tcp->th_dport);
        l4Head->payload = l3Head->payload + p_tcp->th_off * 4;
        l4Head->payload_len = l3Head->payload_len - p_tcp->th_off * 4;
    } else if (l3Head->ip_p == IPPROTO_UDP) {
        if (l3Head->payload_len < sizeof(struct udphdr)) {
            log_err("UDP header Corrupted ");
            goto error;
        }

        struct udphdr *p_udp;
        p_udp = (struct udphdr *) l3Head->payload;
        l4Head->sport = ntohs(p_udp->uh_sport);
        l4Head->dport = ntohs(p_udp->uh_dport);
        l4Head->payload = l3Head->payload + sizeof(struct udphdr);
        l4Head->payload_len = l3Head->payload_len - sizeof(struct udphdr);
    } else if (l3Head->ip_p == 0x1) {//Echo Ping
//        log_warn("ICMP protocol not implemented");
        goto error;
        //Skip now
    } else if (l3Head->ip_p == 0x2) {//IGMP
//        log_warn("IGMP protocol not implemented");
        goto error;
    } else {
        log_warn("IP protocol %x not supported in this version", l3Head->ip_p);
        goto error;
    }

    return l4Head;

    error:
    delete l4Head;
    return nullptr;
}

struct pPcap::packet_meta *pPcap::getPacketMeta(const unsigned char *packet, struct pcap_pkthdr *header) {
    pPcap::l2_head *l2Head = nullptr;
    pPcap::l3_head *l3Head = nullptr;
    pPcap::l4_head *l4Head = nullptr;
    struct packet_meta *c_meta = nullptr;

    l2Head = pPcap::getLayer2(packet, header->caplen);
    if (l2Head == nullptr) {
//        log_warn("layer2 returned null");
        goto error;
    }

    l3Head = pPcap::getLayer3(l2Head);
    if (l3Head == nullptr) {
//        log_warn("layer3 returned null");
        goto error;
    }

    l4Head = pPcap::getLayer4(l3Head);
    if (l4Head == nullptr) {
//        log_warn("layer4 returned null");
        goto error;
    }

    c_meta = (struct packet_meta *) malloc(sizeof(struct packet_meta)); // to extract current meta data;

    c_meta->ether_shost = l2Head->ether_shost;
    c_meta->ether_dhost = l2Head->ether_dhost;
    c_meta->ether_type = l2Head->ether_type;

    c_meta->ip_src = l3Head->ip_src;
    c_meta->ip_dst = l3Head->ip_dst;
    c_meta->ip_p = l3Head->ip_p;
    c_meta->ip_tos = l3Head->ip_tos;

    c_meta->sport = l4Head->sport;
    c_meta->dport = l4Head->dport;


    delete l2Head;
    delete l3Head;
    delete l4Head;

    return c_meta;

    error:
    delete l2Head;
    delete l3Head;
    delete l4Head;

    return nullptr;
}

u_short pPcap::compMac(u_char *mac1, u_char *mac2) {
    /* copied from Steven's UNP */

    int i = ETHER_ADDR_LEN;
    do {
        if (*mac1++ != *mac2++) {
            return 0;
        }
    } while (--i > 0);

    return 1;
}

u_short pPcap::mac_copy(u_char* from, u_char** to){
    if (from== nullptr){
        *to= nullptr;
        return 0;
    }

    *to=(u_char*)malloc(sizeof(u_char)*ETHER_ADDR_LEN);
    check(*to,"Failed to char*");

    int i;

    /* copy data*/
    for( i = 0; i < ETHER_ADDR_LEN; i++ )
        (*to)[i] = (u_char) from[i];

    return 1;

    error:
    return 0;
}

struct pPcap::packet_meta *
pPcap::createPacketMeta(const char *ether_shost, const char *ether_dhost, uint16_t ether_type, uint8_t ip_tos,
                        uint8_t ip_p,
                        const char *ip_src, const char *ip_dst, u_short sport, u_short dport){
    struct pPcap::packet_meta *newMeta = (struct pPcap::packet_meta*)malloc(sizeof(struct pPcap::packet_meta));

    newMeta->ether_shost = pPcap::str2mac(ether_shost);
    newMeta->ether_dhost = pPcap::str2mac(ether_dhost);


    newMeta->ether_type		= ether_type;
    newMeta->ip_tos			= ip_tos; //Type of service.
    newMeta->ip_p			= ip_p; //Protocol.


    newMeta->ip_src = pPcap::str2ip(ip_src);
    newMeta->ip_dst = pPcap::str2ip(ip_dst);

    newMeta->sport=sport;		// source port
    newMeta->dport=dport;		//destination port


    return newMeta;
}

struct pPcap::packet_meta *
pPcap::createPacketMeta(u_char *ether_shost, u_char *ether_dhost, uint16_t ether_type, uint8_t ip_tos, uint8_t ip_p,
                        struct in_addr ip_src, struct in_addr ip_dst, u_short sport, u_short dport) {
    struct pPcap::packet_meta *newMeta = (struct pPcap::packet_meta*)malloc(sizeof(struct pPcap::packet_meta));

    mac_copy(ether_dhost,&newMeta->ether_dhost);
    mac_copy(ether_shost,&newMeta->ether_shost);

    newMeta->ether_type		= ether_type;
    newMeta->ip_tos			= ip_tos; //Type of service.
    newMeta->ip_p			= ip_p; //Protocol.



    newMeta->ip_src = ip_src;
    newMeta->ip_dst = ip_dst;

    newMeta->sport=sport;		// source port
    newMeta->dport=dport;		//destination port


    return newMeta;
}

struct pPcap::packet_meta *
pPcap::createPacketMeta_frm_string(const char *ether_shost, const char  *ether_dhost, const char *ether_type, const char *ip_tos, const char *ip_p,
                        const char *ip_src, const char *ip_dst, const char *sport, const char *dport){
    struct pPcap::packet_meta *newMeta = (struct pPcap::packet_meta*)malloc(sizeof(struct pPcap::packet_meta));


    //Source Mac
    if (strcmp(ether_shost,"*")!=0)
        newMeta->ether_shost = pPcap::str2mac(ether_shost);
    else
        newMeta->ether_shost = nullptr;

    //Dst Mac
    if (strcmp(ether_dhost,"*")!=0)
        newMeta->ether_dhost = pPcap::str2mac(ether_dhost);
    else
        newMeta->ether_dhost = nullptr;

    //ether_type
    if (strcmp(ether_type,"*")!=0)
        newMeta->ether_type = (uint16_t )atoi(ether_type);
    else
        newMeta->ether_type = 0;


    //Type of service.
    if (strcmp(ip_tos,"*")!=0)
        newMeta->ip_tos = (uint8_t )atoi(ip_tos);
    else
        newMeta->ip_tos = 0;

    //Protocol.
    if (strcmp(ip_p,"*")!=0)
        newMeta->ip_p = (uint8_t )atoi(ip_p);
    else
        newMeta->ip_p = 0;

    //Source IP
    if (strcmp(ip_src,"*")!=0)
        newMeta->ip_src = pPcap::str2ip(ip_src);
    else
        newMeta->ip_src = pPcap::str2ip("0.0.0.0");

    //Dst IP
    if (strcmp(ip_dst,"*")!=0)
        newMeta->ip_dst = pPcap::str2ip(ip_dst);
    else
        newMeta->ip_dst = pPcap::str2ip("0.0.0.0");

    //Source port
    if (strcmp(sport,"*")!=0)
        newMeta->sport = (uint8_t )atoi(sport);
    else
        newMeta->sport = 0;

    //Destination port
    if (strcmp(dport,"*")!=0)
        newMeta->dport = (uint8_t )atoi(dport);
    else
        newMeta->dport = 0;

    return newMeta;
}
