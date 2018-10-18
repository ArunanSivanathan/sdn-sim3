//
// Created by Arunan Sivanathan on 27/2/18.
//

#ifndef SDN_SIM3_CLOCK_H
#define SDN_SIM3_CLOCK_H

#include <cstdlib>
#include "logistics.h"
#include <csignal>
#include <ostream>





class SimClockTime{
public:
    explicit SimClockTime(struct timeval *newTime);
    SimClockTime(long sec, long microSec);

    friend std::ostream &operator<<(std::ostream &os, const SimClockTime &clockTime);

    bool operator<(const SimClockTime &rhs) const;

    bool operator>(const SimClockTime &rhs) const;

    bool operator<=(const SimClockTime &rhs) const;

    bool operator>=(const SimClockTime &rhs) const;

    bool operator==(const SimClockTime &rhs) const;

    bool operator!=(const SimClockTime &rhs) const;

    SimClockTime& operator+=(const SimClockTime &rhs);

    char* getFormattedTime(const char* format);

    long getMSec() const;

    void setMSec(long mSec);

    long getMMicroSec() const;

    void setMMicroSec(long mMicroSec);

private:
    long mSec;
    long mMicroSec;
};



class SimClock {
public:

    explicit SimClock(void (*mTickCallBack)(uint32_t upTime,const SimClockTime* cTime ));

    const SimClockTime &getMCurrentTime() const;
    uint32_t setCurrentTime(struct timeval *newTime);
    uint32_t setCurrentTime(SimClockTime newTime);

    uint32_t getUpTime() const;

    void (*mTickCallBack)(uint32_t upTime,const SimClockTime* cTime );

    SimClockTime mTickInterval;
    uint32_t mMaxClockDuration;
    bool mClockUp;

private:
    struct SimClockTime mCurrentTime;
    struct SimClockTime mNextTick;
    uint32_t mUpTime;

    void initializeTime(SimClockTime currentTime);
};


#endif //SDN_SIM3_CLOCK_H
