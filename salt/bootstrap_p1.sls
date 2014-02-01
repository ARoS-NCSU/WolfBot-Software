edimax_driver_32:
    file.managed:
        - name: /lib/modules/3.8.13-bone32/8192cu.ko
        - source: salt://files/lib/modules/3.8.13-bone32/8192cu.ko
    cmd.wait:
        - name: depmod -a
        - watch: 
            - file: /lib/modules/3.8.13-bone32/8192cu.ko

edimax_driver_37:
    file.managed:
        - name: /lib/modules/3.8.13-bone37/8192cu.ko
        - source: salt://files/lib/modules/3.8.13-bone37/8192cu.ko
    cmd.wait:
        - name: depmod -a
        - watch: 
            - file: /lib/modules/3.8.13-bone37/8192cu.ko

/etc/modprobe.d/8192cu.conf:
    file.managed:
        - source: salt://files/etc/modprobe.d/8192cu.conf

/etc/modprobe.d/wifi_blacklist.conf:
    file.managed:
        - source: salt://files/etc/modprobe.d/wifi_blacklist.conf

/etc/modules:
    file.append:
        - text: 8192cu

# kernel upgrade?

/root/.ssh/authorized_keys:
    file.managed:
        - source: salt://files/root/.ssh/authorized_keys

# networking
/etc/network/interfaces:
    file.managed:
        - source: salt://files/etc/network/interfaces

/etc/wpa_supplicant.conf:
    file.managed:
        - source: salt://files/etc/wpa_supplicant.conf

# /etc/dhcp/dhclient.conf ??
/etc/dhcp/dhclient-exit-hooks.d/hostname:
    file.managed:
        - source: salt://files/etc/dhcp/dhclient-exit-hooks.d/hostname

wolfbot:
    file.managed:
        - name: /etc/init.d/wolfbot
        - source: salt://files/etc/init.d/wolfbot
        - mode: 755
    service:
        - enabled

/wolfbot/setup:
    file.recurse:
        - name: /wolfbot/setup
        - source: salt://files/wolfbot/setup
        - clean: True
        - file_mode: 755
        
# vim: set syntax=yaml :
