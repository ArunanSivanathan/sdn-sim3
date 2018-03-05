//
// Created by Arunan Sivanathan on 23/2/18.
//

#ifndef SDN_SIM3_PACKETPARSER_H
#define SDN_SIM3_PACKETPARSER_H

#include <pcap/pcap.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <netinet/if_ether.h>

#include <netinet/ip.h>
#include <netinet/tcp.h>
#include <netinet/udp.h>

namespace pPcap {
    struct packet_meta {
        //Frame
        u_char *ether_dhost;
        u_char *ether_shost;
        uint16_t ether_type;
        //vlanID????
        //Frame

        //IP
        uint8_t ip_tos; //Type of service.
        uint8_t ip_p; //Protocol.
        struct in_addr ip_src; //Source IP address.
        struct in_addr ip_dst; //Destination IP address.
        //IP

        //TCP/UDP
        u_short sport;        // source port
        u_short dport;        //destination port
    };

    struct l2_head {
        u_char *ether_dhost;
        u_char *ether_shost;
        uint16_t ether_type;
        const unsigned char *payload;
        uint32_t payload_len;

    };

    struct l3_head {
        uint8_t ip_tos; //Type of service.
        uint8_t ip_p; //Protocol.
        struct in_addr ip_src; //Source IP address.
        struct in_addr ip_dst; //Destination IP address.
        const unsigned char *payload;
        uint32_t payload_len;
    };

    struct l4_head {
        //TCP/UDP
        u_short sport;        // source port
        u_short dport;        //destination port
        const unsigned char *payload;
        uint32_t payload_len;
    };

    void runParser(char *pcapFile, void (*onNewPacket)(int, const unsigned char *, pcap_pkthdr *));

    struct l2_head *getLayer2(const unsigned char *packet, uint32_t packetSize);

    struct l3_head *getLayer3(pPcap::l2_head *l2Head);

    struct l4_head *getLayer4(pPcap::l3_head *l3Head);

    struct packet_meta *getPacketMeta(const unsigned char *packet, struct pcap_pkthdr *header);

    u_short compMac(u_char *mac1, u_char *mac2);

    u_short mac_copy(u_char *from, u_char **to);

    char *mac2str(u_char *mac);

    char *ip2str(in_addr ip);

    u_char *str2mac(const char *macStr);

    in_addr str2ip(const char *ipStr);

    struct packet_meta *
    createPacketMeta(u_char *ether_shost, u_char *ether_dhost, uint16_t ether_type, uint8_t ip_tos, uint8_t ip_p,
                     struct in_addr ip_src, struct in_addr ip_dst, u_short sport, u_short dport);

    struct packet_meta *
    createPacketMeta(const char *ether_shost, const char *ether_dhost, uint16_t ether_type, uint8_t ip_tos,
                     uint8_t ip_p,
                     const char *ip_src, const char *ip_dst, u_short sport, u_short dport);
}


#endif //SDN_SIM3_PACKETPARSER_H
