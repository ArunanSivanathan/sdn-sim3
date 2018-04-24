#include <iostream>
#include <logistics.h>
#include <pcapParser.h>
#include <SwitchBox.h>
#include "apps/apps.h"

void displayBanner();
void packetInWrapper(int p_no, const unsigned char *packet, struct pcap_pkthdr *header);
void timeTickCallback(uint32_t upTime, const SimClockTime *cTime);

SwitchBox* serviceSwitch;
Controller* mainController;
DataLogger* dataLog;
SimClock* systemClock;

int main(int argc, char *argv[]) {
    /* Skip over the program name. */
    ++argv; --argc;

    /* We expect exactly one argument, the name of the file to dump. */
    if ( argc != 2 ){
        log_err( "program requires two arguments: the trace file, controller app ID\n");
        exit(1);
    }
    // print banner
    displayBanner();

    systemClock = new SimClock(&timeTickCallback);
    dataLog = new DataLogger();
    mainController = apps::getControllerApp(atoi(argv[1]));
    serviceSwitch= new SwitchBox(mainController, dataLog, systemClock);
    mainController->pushInitialRules();

    pPcap::runParser(argv[0], &packetInWrapper);

    delete(serviceSwitch);
    delete(mainController);
    delete(dataLog);

    return 0;
}

void packetInWrapper(int p_no, const unsigned char *packet, struct pcap_pkthdr *header)
{
    serviceSwitch->packetIn(p_no,packet,header);
}

void timeTickCallback(uint32_t upTime, const SimClockTime *cTime) {
    if (upTime%60 == 0)
        serviceSwitch->logFlowActivity(upTime);
    if (upTime%3600 == 0)
        fprintf(stderr, "%06d\r",upTime/3600);
}

void displayBanner(){
    fprintf(stderr," ____  ____  _   _   ____ ___ __  __ \n/ ___||  _ \\| \\ | | / ___|_ _|  \\/  |\n\\___ \\| | | |  \\| | \\___ \\| || |\\/| |\n ___) | |_| | |\\  |  ___) | || |  | |\n|____/|____/|_| \\_| |____/___|_|  |_|\n");

    fprintf(stderr,"\n\n--------------------------------------------------------------\n");
    fprintf(stderr,"\t\t\tWarning\t\t\t\n");
    fprintf(stderr,"* Current version of simulator just work with IP4 packets only\n");
    fprintf(stderr,"* It will ignore all the other packets including ARP and IPV6\n");
    fprintf(stderr,"--------------------------------------------------------------\n\n\n\n\n");
}