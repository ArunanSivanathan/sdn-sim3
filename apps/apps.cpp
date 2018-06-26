//
// Created by Arunan Sivanathan on 1/3/18.
//

#include "apps.h"


Controller *apps::getControllerApp(int appID) {
    Controller* selectedController= nullptr;
    if (appID==0)
        selectedController= new DeviceClassify();
    else if(appID==1)
        selectedController= new SimpleStaticRules();
    else {
        debug("App ID:%D not found. Loading default controller",appID);
        selectedController = new Controller();
    }
    return selectedController;
}

