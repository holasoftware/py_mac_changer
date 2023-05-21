import fcntl
import struct
import socket
import random


"""
This file makes the following assumptions about data structures:

So, you need few things to change the MAC:


IFNAMSIZ is defined to be 16 bytes, so 15 user-visible bytes (assuming it includes a trailing null). It's defined in linux/if.h

struct ifreq {
   char ifr_name[IFNAMSIZ]; /* Interface name */
   union {
       struct sockaddr ifr_addr;
       struct sockaddr ifr_dstaddr;
       struct sockaddr ifr_broadaddr;
       struct sockaddr ifr_netmask;
       struct sockaddr ifr_hwaddr;
       short           ifr_flags;
       int             ifr_ifindex;
       int             ifr_metric;
       int             ifr_mtu;
       struct ifmap    ifr_map;
       char            ifr_slave[IFNAMSIZ];
       char            ifr_newname[IFNAMSIZ];
       char           *ifr_data;
   };
};


typedef unsigned short sa_family_t;

struct sockaddr {
    sa_family_t  sa_family;
    char         sa_data[14];
};

See man netdevice
"""

# From linux/if_arp.h
ARPHRD_ETHER = 1

# From linux/sockios.h
SIOCSIFHWADDR = 0x8924
SIOCGIFHWADDR = 0x8927


def get_random_mac_address():
    mac = [ 0x00, 0x16, 0x3e,
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
        
    return ':'.join(map(lambda x: "%02x" % x, mac))


def change_mac_address(ifr_name, newmac):
    # The hardware address is specified in a struct sockaddr. sa_family contains the ARPHRD_* device type. See above note about data structures.
    # ifr_name (must be nul terminated string)
    # An Ethernet MAC address is a 48-bit address. Because 1 byte equals 8 bits, we can also say that a MAC address is 6 bytes in length.

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    macbytes = [int(i, 16) for i in newmac.split(':')]
    ifreq = struct.pack('16sH6B8x', bytes(ifr_name, 'utf-8')[:15], ARPHRD_ETHER, *macbytes)
    fcntl.ioctl(s.fileno(), SIOCSIFHWADDR, ifreq)


def get_current_mac_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), SIOCGIFHWADDR,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Python Mac Changer for Linux")
    parser.add_argument("interface", help="The network interface name on Linux")
    parser.add_argument("-m", "--mac", help="The new MAC you want to change using this separator ':'")
    args = parser.parse_args()

    iface = args.interface

    if args.mac:
        # if mac is set, use it instead
        new_mac_address = args.mac
    else:
        new_mac_address = get_random_mac_address()
        
    # get the current MAC address
    old_mac_address = get_current_mac_address(iface)
    print("[*] Old MAC address:", old_mac_address)

    # change the MAC address
    change_mac_address(iface, new_mac_address)
    new_mac_address = get_current_mac_address(iface)
    print("[+] New MAC address:", new_mac_address)
    
    
if __name__ == "__main__":
    main()

