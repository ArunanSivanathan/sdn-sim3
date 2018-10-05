#include <iostream>
#include <logistics.h>
#include <pcapParser.h>
#include <SwitchBox.h>
#include "apps/apps.h"
#include "main.h"
#include "config.h"

void displayBanner();
void packetInWrapper(int p_no, const unsigned char *packet, struct pcap_pkthdr *header);
void timeTickCallback(uint32_t upTime, const SimClockTime *cTime);

SwitchBox* serviceSwitch;
Controller* mainController;
DataLogger* dataLog;
SimClock* systemClock;

int main(int argc, char *argv[]) {
    /* Skip over the program name. */

    /** Read program arguments **/
    char  *argPcap;
    resolution = 60;
    char **ctrloptv;
    int ctrloptc=0;
    output_log="./";

    int c;
    while (1) {
        int option_index = 0;

        c = getopt_long (argc, argv, "r:c:o:", long_options, &option_index);
        /* Detect the end of the options. */
        if (c == -1)
            break;

        switch (c) {
            case 0:
                if (long_options[option_index].flag != 0)
                    break;
                printf("option %s", long_options[option_index].name);
                if (optarg)
                    printf(" with arg %s", optarg);
                printf("\n");
                break;
            case 'o':
                output_log = string(optarg);
            case 'r':
                resolution = atoi(optarg);
                break;
            case '?':
                /* getopt_long already printed an error message. */
                if (optopt == 'r')
                    log_err("Option -%c requires an argument.\n", optopt);
                else
                    printAppUsage();
                break;
            default:
                abort();
        }

    };
    //todo: allow to pass log directory


    /* Read PCAP path */
    if (optind >= argc){
        log_err("No source pcap file found in argument\n");
        printAppUsage();
        exit(EXIT_FAILURE);
    }

    argPcap = argv[optind];
    ctrloptc = argc - (optind+1);
    ctrloptv = &argv[optind+1];

    optind=0; //Reset argument counter


    // print banner
    displayBanner();

    verbose("Simulator output resolution\t:\t%d Sec",resolution);
    verbose("Input PCAP\t:\t%s",argPcap);


    systemClock = new SimClock(&timeTickCallback);
    dataLog = new DataLogger();
    mainController = apps::getControllerApp(ctrloptc, ctrloptv);
    serviceSwitch= new SwitchBox(mainController, dataLog, systemClock);
    mainController->pushInitialRules();

    pPcap::runParser(argPcap, &packetInWrapper);

    delete(serviceSwitch);
    delete(mainController);
    delete(dataLog);

    return 0;
}

void printAppUsage(){
    std::cerr<<"usage: sdn_sim3 [options] <pcap_path> [<controller_id>] [-- <controller_options...>]"<<std::endl;
    std::cerr<<"options:"<<std::endl;
    std::cerr<<" --verbose\tverbose output"<<std::endl;
    std::cerr<<" --brief\tbrief output"<<std::endl;
    std::cerr<<" -r, --resolution=<T>\tLogging resolution in Secs[default:60]"<<std::endl;
    std::cerr<<std::endl<<std::endl;
    std::cerr<<"Controllers:"<<std::endl;
    std::cerr<<" ofdc\t\t\tOpenflow device classification"<<std::endl;
    std::cerr<<" simplestatic\tSimple static flows"<<std::endl;
    exit(EXIT_FAILURE);
}

void packetInWrapper(int p_no, const unsigned char *packet, struct pcap_pkthdr *header)
{
    serviceSwitch->packetIn(p_no,packet,header);
}

void timeTickCallback(uint32_t upTime, const SimClockTime *cTime) {
    if (upTime%resolution == 0) {
        if (FLOW_ACTIVITY_WITH_EPOCH_TIME)
            serviceSwitch->logFlowActivity(cTime->getMSec());
        else
            serviceSwitch->logFlowActivity(upTime);

    }
    if (upTime%3600 == 0) {
        fprintf(stdout, "%06d\r", upTime / 3600);
        std::cout.flush();
    }
}

void displayBanner(){
    std::cout <<" ____  ____  _   _   ____ ___ __  __ \n/ ___||  _ \\| \\ | | / ___|_ _|  \\/  |\n\\___ \\| | | |  \\| | \\___ \\| || |\\/| |\n ___) | |_| | |\\  |  ___) | || |  | |\n|____/|____/|_| \\_| |____/___|_|  |_|\n";

    std::cout <<"\n\n--------------------------------------------------------------\n";
    std::cout <<"\t\t\tWarning\t\t\t\n";
    std::cout <<"* Current version of simulator just work with IP4 packets only\n";
    std::cout <<"* It will ignore all the other packets including ARP and IPV6\n";
    std::cout <<"--------------------------------------------------------------\n\n\n\n\n";
    std::cout.flush();
}