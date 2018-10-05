//
// Created by Arunan Sivanathan on 3/10/18.
//

#include "IPaddress.h"

static int8_t asciiToHex(char c) {
    c |= 0x20;

    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'a' && c <= 'f') {
        return (c - 'a') + 10;
    } else {
        return -1;
    }
}

/********************* IPv6 *********************/

IPv6::IPv6() {
    memset(_address, 0, sizeof(_address));
}

bool IPv6::operator==(const IPv6 &rhs) const {
    for (int i = 0; i < _bytecount; i++) {
        if (_address[i] != rhs._address[i])
            return false;
    }
    return true;
}

bool IPv6::operator!=(const IPv6 &rhs) const {
    return !(rhs == *this);
}

bool IPv6::fromBytes(const unsigned char *addrbyte) {
    for (int i = 0; i < _bytecount; i++) {
        _address[i] = addrbyte[i];
    }
    return true;
}

std::string IPv6::to_string() const {
    char buf[MAX_IPV6_ADDRESS_STR_LEN + 1 + 1];//Additional 1 byte for snprintf \0.
    for (int i = 0; i < _bytecount; i += 2) {
        snprintf(buf + i / 2 * 5, 6, "%02x%02x:", (int) this->_address[i], (int) this->_address[i + 1]);
    }
    buf[MAX_IPV6_ADDRESS_STR_LEN] = '\0';
    return std::string(buf);
}

std::ostream &operator<<(std::ostream &os, const IPv6 &_ipv6) {
    os << _ipv6.to_string();
    return os;
}

bool IPv6::fromString(const char *addrstr) {
    uint16_t accumulator = 0;
    uint8_t colon_count = 0;
    uint8_t pos = 0;

    memset(_address, 0, sizeof(_address));

    // Step 1: look for position of ::, and count colons after it
    for (uint8_t i = 1; i <= MAX_IPV6_ADDRESS_STR_LEN; i++) {
        if (addrstr[i] == ':') {
            if (addrstr[i - 1] == ':') {
                // Double colon!
                colon_count = 14;
            } else if (colon_count) {
                // Count backwards the number of colons after the ::
                colon_count -= 2;
            }
        } else if (addrstr[i] == '\0') {
            break;
        }
    }

    // Step 2: convert from ascii to binary
    for (uint8_t i = 0; i <= MAX_IPV6_ADDRESS_STR_LEN && pos < 16; i++) {
        if (addrstr[i] == ':' || addrstr[i] == '\0') {
            _address[pos] = accumulator >> 8;
            _address[pos + 1] = accumulator;
            accumulator = 0;

            if (colon_count && i && addrstr[i - 1] == ':') {
                pos = colon_count;
            } else {
                pos += 2;
            }
        } else {
            int8_t val = asciiToHex(addrstr[i]);
            if (val == -1) {
                // Not hex or colon: fail
                return 0;
            } else {
                accumulator <<= 4;
                accumulator |= val;
            }
        }

        if (addrstr[i] == '\0')
            break;
    }

    // Success
    return 1;
}

IPv6 &IPv6::operator=(IPv6 _pv6) {
    for (int i = 0; i < this->_bytecount; i++) {
        this->_address[i] = _pv6._address[i];
    }
    return *this;
}


/********************* IPv4 *********************/
IPv4::IPv4() {
    memset(_address, 0, sizeof(_address));
}

bool IPv4::fromBytes(const unsigned char *addrbyte) {
    for (int i = 0; i < _bytecount; i++) {
        _address[i] = addrbyte[i];
    }
    return true;
}

std::string IPv4::to_string() const {
    int buf_length = MAX_IPV4_ADDRESS_STR_LEN + 1 + 1;
    char buf[buf_length];//Additional 1 byte for snprintf \0.
    int buf_point = 0;
    for (int i = 0; i < _bytecount; i += 1) {
        buf_point += snprintf(buf + buf_point, buf_length - buf_point, "%d.", (int) this->_address[i]);
    }
    buf[buf_point-1] = '\0';
    return std::string(buf);
}

bool IPv4::operator==(const IPv4 &rhs) const {
    for (int i = 0; i < _bytecount; i++) {
        if (_address[i] != rhs._address[i])
            return false;
    }
    return true;
}

bool IPv4::operator!=(const IPv4 &rhs) const {
    return !(rhs == *this);
}

std::ostream &operator<<(std::ostream &os, const IPv4 &pv4) {
    os << pv4.to_string();
    return os;
}

IPv4 &IPv4::operator=(IPv4 _pv4) {
    for (int i = 0; i < this->_bytecount; i++) {
        this->_address[i] = _pv4._address[i];
    }
    return *this;
}

bool IPv4::fromString(const char *addrstr) {
    sscanf(addrstr, "%hu.%hu.%hu.%hu", (unsigned short *) &_address[0], (unsigned short *) &_address[1],
           (unsigned short *) &_address[2], (unsigned short *) &_address[3]);
    return true;
}