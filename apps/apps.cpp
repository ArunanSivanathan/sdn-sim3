//
// Created by Arunan Sivanathan on 1/3/18.
//

#include "apps.h"


Controller *apps::getControllerApp(int ctrloptc, char *ctrloptv[]) {
    Controller* selectedController= nullptr;
    if (ctrloptc == 0){
        verbose("No controller specified. Loading default controller");
        selectedController = new Controller();
    }


    if (strcmp(ctrloptv[0],"ofdc")== 0)
        selectedController= new DeviceClassify();
    else if(strcmp(ctrloptv[0],"simplestatic") == 0)
        selectedController= new SimpleStaticRules();
    else {
        debug("App ID:%s not found. Loading default controller",ctrloptv[0]);
        selectedController = new Controller();
    }
    return selectedController;
}

