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
            - python-numpy
            - python-scipy

saltstack_repo:
  pkgrepo.managed:
    - name: deb http://debian.saltstack.com/debian wheezy-saltstack main
    - file: /etc/apt/sources.list.d/saltstack.list
    - gpgkey: http://debian.saltstack.com/debian-salt-team-joehealy.gpg.key 
    - require_in:
        - pkg: salt-minion
    - require:
        - pkg: python-apt

salt-minion:
    pkg.latest:
        - skip_verify: True
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/salt/minion

/etc/salt/minion:
    file.managed:
        - source: salt://files/etc/salt/minion

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

# NB: if the above fails, make sure the uSD card has been remvoed!
#     (otherwise rootfs may be multi-valued)

# KERNEL

# set a variable instead of repeating kernel number?
edimax_driver_26:
    file.managed:
        - name: /lib/modules/3.8.13-bone26/8192cu.ko
        - source: salt://files/lib/modules/3.8.13-bone26/8192cu.ko
    cmd.wait:
        - name: depmod -a
        - watch: 
            - file: /lib/modules/3.8.13-bone26/8192cu.ko

edimax_driver_32:
    file.managed:
        - name: /lib/modules/3.8.13-bone32/8192cu.ko
        - source: salt://files/lib/modules/3.8.13-bone32/8192cu.ko
    cmd.wait:
        - name: depmod -a
        - watch: 
            - file: /lib/modules/3.8.13-bone32/8192cu.ko

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

# only install during bootstrap?
/etc/salt/pki/minion/minion_master.pub:
    file.managed:
        - source: salt://files/etc/salt/pki/minion/minion_master.pub

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
        
/wolfbot/demos:
    file.recurse:
        - name: /wolfbot/demos
        - source: salt://files/wolfbot/demos
        - clean: True
        - file_mode: 755
        
/wolfbot/lib:
    file.recurse:
        - name: /wolfbot/lib
        - source: salt://files/wolfbot/lib
        - clean: True
        - file_mode: 755
        
    
# ssh keys


# vim: set syntax=yaml :
