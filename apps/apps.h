//
// Created by Arunan Sivanathan on 1/3/18.
//



#ifndef SDN_SIM3_APPS_H
#define SDN_SIM3_APPS_H
#include <controller.h>
#include "DeviceClassify.h"
#include "SimpleStaticRules.h"
#endif //SDN_SIM3_APPS_H
namespace apps {
    Controller *getControllerApp(int appID);
}