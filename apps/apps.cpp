//
// Created by Arunan Sivanathan on 1/3/18.
//

#include "apps.h"


Controller *apps::getControllerApp(int ctrloptc, char *ctrloptv[]) {
    Controller* selectedController= nullptr;
    if (ctrloptc == 0){
        verbose("No controller specified. Loading default controller");
        selectedController = new Controller(ctrloptc,ctrloptv);
    }

    if (strcmp(ctrloptv[0],"ofdc")== 0)
        selectedController= new DeviceClassify(ctrloptc,ctrloptv);
    else if(strcmp(ctrloptv[0],"simplestatic") == 0)
        selectedController= new SimpleStaticRules(ctrloptc,ctrloptv);
    else if(strcmp(ctrloptv[0],"dnsparser") == 0)
        selectedController= new DNSParser(ctrloptc,ctrloptv);
    else {
        debug("App ID:%s not found. Loading default controller",ctrloptv[0]);
        selectedController = new Controller(ctrloptc,ctrloptv);
    }
    return selectedController;
}

