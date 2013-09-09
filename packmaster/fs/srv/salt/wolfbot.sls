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
        - source: salt://fs/etc/ntp.conf
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
        - source: salt://fs/etc/ffserver.conf

/boot/uboot/uEnv.txt:
    file.managed:
        - source: salt://fs/boot/uboot/uEnv.txt
        - template: jinja
        - context: 
            uuid: {{ grains['fs_uuid']['rootfs'] }}

# kernel stuff

# set a variable instead of repeating kernel number?
edimax_driver:
    file.managed:
        - name: /lib/modules/3.8.13-bone26/8192cu.ko
        - source: salt://fs/lib/modules/3.8.13-bone26/8192cu.ko
    cmd.wait:
        - name: depmod -a
        - watch: 
            - file: /lib/modules/3.8.13-bone26/8192cu.ko

/etc/modprobe.d/8192cu.conf:
    file.managed:
        - source: salt://fs/etc/modprobe.d/8192cu.conf

/etc/modprobe.d/wifi_blacklist.conf:
    file.managed:
        - source: salt://fs/etc/modprobe.d/wifi_blacklist.conf

/etc/modules:
    file.append:
        - text: 8192cu

# kernel upgrade?

# networking
/etc/network/interfaces:
    file.managed:
        - source: salt://fs/etc/network/interfaces

/etc/wpa_supplicant.conf:
    file.managed:
        - source: salt://fs/etc/wpa_supplicant.conf
    
# /etc/dhcp

# wolfbot startup script
# wolfbot software
# ssh keys


# vim: set syntax=yaml :
