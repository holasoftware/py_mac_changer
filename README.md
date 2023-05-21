Mac changer in pure python without using ifconfig, using ioctl system call. Setting the hardware address is a privileged operation. To execute this utility you will need sudo privilegies or to be root.

To change to a random mac address just use:
```
    sudo python3 py_mac_changer.py <interface_name>
```
To set a specific mac address:
```
    sudo python3 py_mac_changer.py <interface_name> -mac <mac_address>
```

To list the names of your device interfaces:
```
    ip link show
```

Stop your network manager:
```
    sudo service network-manager stop
```
or disconnect from your network device before changing the mac address.

To start again the service:
```
    sudo service network-manager start
```
