en_US.UTF-8:
    locale.system

America/New_York:
    timezone.system:
        - utc: True

ntp:
    pkg:
        - installed
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/ntp.conf
    file.managed:
        - name: /etc/ntp.conf
        - source: salt://files/etc/ntp.conf
        - user: root
        - group: root
        - mode: 644

vim:
    pkg.installed

bind9-host:
    pkg.installed

wolfbot_python_reqs:
    pkg.installed:
        - pkgs:
            - ipython
            - python-yaml
            - python-smbus

deb-multimedia-keyring:
    pkg.latest:
        - skip_verify: true
    cmd.wait:
        - name: apt-get update > /dev/null
        - watch: 
            - pkg: deb-multimedia-keyring

deb-multimedia:
  pkgrepo.managed:
    - name: deb http://www.deb-multimedia.org wheezy main non-free
    - file: /etc/apt/sources.list.d/debian-multimedia.list
    - require_in:   # per the docs, can't use a require line in ffmpeg instead
      - pkg: deb-multimedia-keyring
      - pkg: ffmpeg
    - require:
        - pkg: python-apt

python-apt:
    pkg.installed

ffmpeg:
    pkg:
        - installed
    file.managed:
        - name: /etc/ffserver.conf
        - source: salt://files/etc/ffserver.conf

/boot/uboot/uEnv.txt:
    file.managed:
        - source: salt://files/boot/uboot/uEnv.txt
        - template: jinja
        - context: 
            uuid: {{ grains['fs_uuid']['rootfs'] }}

# KERNEL

# set a variable instead of repeating kernel number?
edimax_driver:
    file.managed:
        - name: /lib/modules/3.8.13-bone26/8192cu.ko
        - source: salt://files/lib/modules/3.8.13-bone26/8192cu.ko
    cmd.wait:
        - name: depmod -a
        - watch: 
            - file: /lib/modules/3.8.13-bone26/8192cu.ko

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

/wolfbot/agent:
    file.recurse:
        - name: /wolfbot/agent
        - source: salt://files/wolfbot/agent  # change to github tree on pm?
        - clean: True
        
/wolfbot/config:
    file.recurse:
        - name: /wolfbot/config
        - source: salt://files/wolfbot/config
        - clean: True
        
/wolfbot/setup:
    file.recurse:
        - name: /wolfbot/setup
        - source: salt://files/wolfbot/setup
        - clean: True
        - file_mode: 755
        
/wolfbot/util:
    file.recurse:
        - name: /wolfbot/util
        - source: salt://files/wolfbot/util
        - clean: True
        - file_mode: 755
        
    
# ssh keys


# vim: set syntax=yaml :
