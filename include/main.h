//
// Created by Arunan Sivanathan on 28/6/18.
//

#ifndef SDN_SIM3_MAIN_H
#include <getopt.h>
#include "config.h"
/* Flag set by ‘--verbose’. */

int verboseFlag;
int resolution;
std::string output_log;

struct option long_options[] =
        {
                /* These options set a flag. */
                {"verbose", no_argument,       &verboseFlag, 1},
                {"brief",   no_argument,       &verboseFlag, 0},
                /* These options don’t set a flag.
                   We distinguish them by their indices. */
                {"resolution",  required_argument, 0, 'r'},
                {"output",  required_argument, 0, 'o'},
                {0, 0, 0, 0}
        };

void printAppUsage();


#define SDN_SIM3_MAIN_H



#endif //SDN_SIM3_MAIN_H
