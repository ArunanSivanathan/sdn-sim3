//
// Created by Arunan Sivanathan on 3/5/18.
//

#ifndef SDN_SIM3_SIMPLESTATICRULES_H
#define SDN_SIM3_SIMPLESTATICRULES_H

#include <controller.h>
#include <vector>
#include <fstream>
#include <getopt.h>



class SimpleStaticRules : public Controller {
public:
    typedef std::vector<std::string> char_vec_t;

    SimpleStaticRules(int ctrloptc, char **ctrloptv);

    SwitchBox *getServiceSwitch() const override {
        return Controller::getServiceSwitch();
    }

    void pushInitialRules() override;

    int readnPush(const char *filePath);
private:
    char* flow_entry_file;
};
#endif //SDN_SIM3_SIMPLESTATICRULES_H
