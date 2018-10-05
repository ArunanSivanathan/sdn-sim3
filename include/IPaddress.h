//
// Created by Arunan Sivanathan on 3/10/18.
//

#ifndef SDN_SIM3_IPADDRESS_H
#define SDN_SIM3_IPADDRESS_H


#include <string>
#include <ostream>

#define MAX_IPV6_ADDRESS_STR_LEN  39
#define MAX_IPV4_ADDRESS_STR_LEN 15

static int8_t asciiToHex(char c);

class IPaddr{
public:
    virtual bool fromBytes(const unsigned char *addrbyte) = 0;
    virtual std::string to_string() const = 0 ;
};

class IPv6: public IPaddr{
public:
    IPv6();
    bool fromBytes(const unsigned char *addrbyte) override;
    std::string to_string() const override;
    bool fromString(const char *addrstr);

    bool operator==(const IPv6 &rhs) const;
    bool operator!=(const IPv6 &rhs) const;
    IPv6& operator=(IPv6 _pv6);

    friend std::ostream &operator<<(std::ostream &os, const IPv6 &pv6);

    const short _bytecount = 16;


private:
    unsigned char _address[16];
};

class IPv4: public IPaddr{
public:
    IPv4();

    bool fromBytes(const unsigned char *addrbyte) override;
    std::string to_string() const override;
    bool fromString(const char *addrstr);

    friend std::ostream &operator<<(std::ostream &os, const IPv4 &pv4);

    bool operator==(const IPv4 &rhs) const;
    bool operator!=(const IPv4 &rhs) const;
    IPv4& operator=(IPv4 _pv4);
    const short _bytecount = 4;

private:
    unsigned char _address[4];
};



#endif //SDN_SIM3_IPADDRESS_H
