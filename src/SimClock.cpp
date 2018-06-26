//
// Created by Arunan Sivanathan on 27/2/18.
//



#include "SimClock.h"

SimClock::SimClock(void (*mTickCallBack)(uint32_t upTime,const SimClockTime* cTime )) : mTickInterval(1,0),mCurrentTime(0,0),mNextTick(0,0) {
    this->mUpTime = 0;
    this->mTickCallBack = mTickCallBack;
    this->mClockUp = false;
    this->mMaxClockDuration=100000;
}

void SimClock::initializeTime(SimClockTime currentTime) {
    // Set the first packet second as starting time
    mCurrentTime=currentTime;
    mCurrentTime.setMMicroSec(0);//To debug
    mNextTick = mCurrentTime;
    mNextTick +=mTickInterval;//Increase to next tick
    mClockUp = true;
    mTickCallBack(mUpTime,&mCurrentTime);
}

uint32_t SimClock::setCurrentTime(struct timeval *newTime){
    return setCurrentTime(SimClockTime(newTime));
}

uint32_t SimClock::setCurrentTime(SimClockTime newTime) {
    // Initialize timer
    if (mClockUp == false) {
        initializeTime(newTime);
    }

    //Do until current packet come in frame

    // printtime(newTime,"Current time");
    // printtime(newTime,"Packet time");
    // printtime(mNextTick,"Next time\n");

    if (mCurrentTime > newTime) {//If wrong time Identified on packet
        log_err("Time went back in clock! That means you found a way for time travel!");
        log_err("%l",newTime.getMSec());
//        raise(SIGILL); //Signal Illegal Instruction
        return mUpTime;
    }

    if (mUpTime > mMaxClockDuration) {//If wrong time Identified on packet
        log_err("Clock was working for too long time!");
        log_err("%l",newTime.getMSec());
        raise(SIGILL); //Signal Illegal Instruction
    }

    while (!(mCurrentTime<= newTime && mNextTick > newTime)) { //tick event until you find the correct time slot
        //Slide to next frame
        mCurrentTime = mNextTick;
        mNextTick += mTickInterval;
        mUpTime += 1;
        mTickCallBack(mUpTime,&mCurrentTime);

    }

    return mUpTime;
}


uint32_t SimClock::getUpTime() const {
    return mUpTime;
}

const SimClockTime &SimClock::getMCurrentTime() const {
    return mCurrentTime;
}


/***SimClockTime ***/
SimClockTime::SimClockTime(struct timeval *tv):SimClockTime(tv->tv_sec, tv->tv_usec) {}

SimClockTime::SimClockTime(long sec, long microSec) {
    mSec = sec;
    mMicroSec = microSec;
}

bool SimClockTime::operator<(const SimClockTime &rhs) const {
    return (this->mSec < rhs.mSec) || ((this->mSec == rhs.mSec) && (this->mMicroSec < rhs.mMicroSec));
}

bool SimClockTime::operator>(const SimClockTime &rhs) const {
    return rhs < *this;
}

bool SimClockTime::operator<=(const SimClockTime &rhs) const {
    return !(rhs < *this);
}

bool SimClockTime::operator>=(const SimClockTime &rhs) const {
    return !(*this < rhs);
}

bool SimClockTime::operator==(const SimClockTime &rhs) const {
    return mSec == rhs.mSec &&
           mMicroSec == rhs.mMicroSec;
}

bool SimClockTime::operator!=(const SimClockTime &rhs) const {
    return !(rhs == *this);
}

std::ostream &operator<<(std::ostream &os, const SimClockTime &clockTime) {
    os << "mSec: " << clockTime.mSec << " mMicroSec: " << clockTime.mMicroSec;
    return os;
}

SimClockTime& SimClockTime::operator+=(const SimClockTime &rhs) {
    this->mSec = this->mSec + rhs.mSec + ((this->mMicroSec + rhs.mMicroSec)/1000000);
    this->mMicroSec = (this->mMicroSec + rhs.mMicroSec)%1000000;

    return *this;
}

char *SimClockTime::getFormattedTime(char* format) {
    char* ts_buffer;
    ts_buffer= (char*)malloc(sizeof(char)* 256);

    struct tm *nowtm;//Time in readable format
    nowtm = localtime(&(this->mSec));

    char tmbuf[64];
    strftime(tmbuf, sizeof tmbuf, format, nowtm);


    sprintf(ts_buffer, "%s.%06d",tmbuf, (int) this->mSec);

    return ts_buffer;

}

long SimClockTime::getMSec() const {
    return mSec;
}

void SimClockTime::setMSec(long mSec) {
    SimClockTime::mSec = mSec;
}

long SimClockTime::getMMicroSec() const {
    return mMicroSec;
}

void SimClockTime::setMMicroSec(long mMicroSec) {
    SimClockTime::mMicroSec = mMicroSec;
}
