//
// Created by Arunan Sivanathan on 3/5/18.
// --verbose -r 60 "/Users/Arunan/Documents/PCAP-Transfer/under_process/activity/18-06-26.pcap" simplestatic -- --flowentries ../config/simplestatic_flows.txt
//


#include "SimpleStaticRules.h"
#include <algorithm>    // copy
#include <iterator>     // back_inserter
#include <regex>        // regex, sregex_token_iterator
#include <iostream>

SimpleStaticRules::SimpleStaticRules(int ctrloptc, char **ctrloptv) : Controller(ctrloptc, ctrloptv) {

    struct option app_options[] =
            {
                    {"flowentries", required_argument, 0, 'e'},
                    {0, 0,                             0, 0}
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
            case 'e':
                flow_entry_file = optarg;
                verbose("Flowenties are being loaded from \"%s\"", flow_entry_file)
                break;
            case '?':
                /* getopt_long already printed an error message. */
                if (optopt == 'r')
                    log_err("Option -%c requires an argument.\n", optopt);
                break;
            default:
                abort();
        }

    };

}


void SimpleStaticRules::pushInitialRules() {
    log_info("Initializing SimpleStaticRules controller");
    Controller::pushInitialRules();
    //todo:read from json file
    this->readnPush(flow_entry_file);
}


//void SimpleStaticRules::trackFaceTimeAudioCall() {
//    struct pPcap::packet_meta *r;
//    // Facetime out
////    26139	2018-05-03 16:58:04	ac:bc:32:d4:6f:2f	00:00:0c:9f:fa:f2	10.248.46.101		16393	3494	STUN	ChannelData TURN Message
//
//    char ip_address[][16]= {"17.120.252.12", "17.120.252.13", "17.125.249.10", "17.125.249.11", "17.154.66.159", "17.253.67.201",
//                "17.253.67.202", "17.253.67.204", "17.253.67.205", "17.253.67.208", "23.77.128.53", "23.77.131.226",
//                "23.77.151.183", "23.77.153.183"};
//
//    int i;
//    for (i = 0;i<14;i++) {
//        r = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, (char *) ip_address[i], (char *) "0.0.0.0", 0, 0);
//        getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);
//        r = pPcap::createPacketMeta(nullptr, nullptr, 0, 0, 0, (char *) "0.0.0.0", (char *) ip_address[i], 0, 0);
//        getServiceSwitch()->flowrulePush(1 << 4, r, FORWARD, 0);
//    }
//
//
//}

int SimpleStaticRules::readnPush(const char *filePath) {
    //Todo: double check memory leaks

    std::ifstream inFile;
    std::vector<std::string> vec;

    std::string mac_match_condition = "((?:[a-f|A-F|\\d]{2}:){5}(?:[a-f|A-F|\\d]{2})|\\*)";
    std::string ip_match_condition = "(\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}|\\*)";
    std::string integer_condition = "(\\d+|\\*)";
    std::string delimiter_condition = "\\s*,\\s*";

    std::string full_condition;
    full_condition = "^\\s*";
    full_condition += mac_match_condition + delimiter_condition;
    full_condition += mac_match_condition + delimiter_condition;
    full_condition += integer_condition + delimiter_condition;
    full_condition += integer_condition + delimiter_condition;
    full_condition += integer_condition + delimiter_condition;
    full_condition += ip_match_condition + delimiter_condition;
    full_condition += ip_match_condition + delimiter_condition;
    full_condition += integer_condition + delimiter_condition;
    full_condition += integer_condition + delimiter_condition;
    full_condition += integer_condition;
    full_condition += "\\s*$";

    std::regex re_csv_match(full_condition.c_str());
//    cerr << full_condition;

    inFile.open(filePath);
    if (!inFile.is_open()) {
        log_err("Flow entry file cannot be opened");
        exit(EXIT_FAILURE);
    }
    std::string line = "";

    int line_seek = 0;

    std::smatch cm;
    struct pPcap::packet_meta *r;

    while (getline(inFile, line)) {
        line_seek++;
        if (line_seek == 1)
            continue;

        if (regex_match(line, re_csv_match)) {
            regex_match(line, cm, re_csv_match);

            const char* s_mac = cm.str(1).c_str();
            const char* d_mac = cm.str(2).c_str();
            const char* ether_type = cm.str(3).c_str();
            const char* ip_tos = cm.str(4).c_str();
            const char* ip_p = cm.str(5).c_str();
            const char* ip_src = cm.str(6).c_str();
            const char* ip_dst = cm.str(7).c_str();
            const char* sport = cm.str(8).c_str();
            const char* dport = cm.str(9).c_str();
            const char* priority = cm.str(10).c_str();

            r = pPcap::createPacketMeta_frm_string(s_mac, d_mac, ether_type,
                                                   ip_tos, ip_p, ip_src,
                                                   ip_dst, sport, dport);

//            delete  s_mac;
//            delete d_mac;
//            delete ether_type;
//            delete ip_tos;
//            delete ip_p;
//            delete ip_src;
//            delete ip_dst;
//            delete sport;
//            delete dport;


            getServiceSwitch()->flowrulePush(std::strtol (priority, nullptr,10), r, FORWARD, 0);

            //for (unsigned i=0; i<cm.size(); ++i) {
            //    std::cerr << i <<"[" << cm[i] << "] "<<endl;
            //  }
        } else {
            log_err("Flowentry format mismatch: %s", line.c_str());
        }
//        exit(EXIT_SUCCESS);
        verbose("%d)\t%s", line_seek, line.c_str());
    }

    inFile.close();
    return 0;
}

