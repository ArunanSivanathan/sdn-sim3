//
// Created by Arunan Sivanathan on 23/2/18.
//

#include "logistics.h"

char* etime::timestamp_string(struct timeval *ts) {
    char* timestamp_string_buf;
    timestamp_string_buf = (char*)malloc(sizeof(char)*256);


    struct tm *nowtm;//Time in readable format
    char tmbuf[64];


    nowtm = localtime(&(ts->tv_sec));
    strftime(tmbuf, sizeof tmbuf, "%Y-%m-%d %H:%M:%S", nowtm);

    sprintf(timestamp_string_buf, "%s.%06d",tmbuf, (int) ts->tv_usec);

    return timestamp_string_buf;
}
