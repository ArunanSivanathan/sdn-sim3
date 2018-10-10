//
// Created by Arunan Sivanathan on 26/2/18.
//

#ifndef SDN_SIM3_CONTROLLER_H
#define SDN_SIM3_CONTROLLER_H


#include "SwitchBox.h"

class SwitchBox;
class DataLogger;

class Controller {
public:


    explicit Controller(int ctrloptc, char *ctrloptv[]);

    virtual SwitchBox *getServiceSwitch() const;

    virtual void setServiceSwitch(SwitchBox *serviceSwitch);

    DataLogger *getMDataLogger() const;

    void setMDataLogger(DataLogger *mDataLogger);

    virtual ushort toController(pPcap::sim_pack *new_packet, struct pPcap::packet_meta *p_m);

    virtual void mirroredTraffic(pPcap::sim_pack *new_packet, int opt);

    virtual void pushInitialRules();

private:
    DataLogger* mDataLogger;
    SwitchBox* mServiceSwitch;

};


#endif //SDN_SIM3_CONTROLLER_H
