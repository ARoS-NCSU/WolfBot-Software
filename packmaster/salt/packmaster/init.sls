en_US.UTF-8:
    locale.system

America/New_York:
    timezone.system:
        - utc: True

saltstack_repo:
  pkgrepo.managed:
    - name: deb http://debian.saltstack.com/debian wheezy-saltstack main
    - file: /etc/apt/sources.list.d/saltstack.list
    - gpgkey: http://debian.saltstack.com/debian-salt-team-joehealy.gpg.key 
    - require_in:
        - pkg: salt-master
    - require:
        - pkg: python-apt

python-apt:
    pkg.installed

# Currently using skip_verify to handle unverified packages. Should fix by updating keyring, e.g.:
#   wget -q -O- "http://debian.saltstack.com/debian-salt-team-joehealy.gpg.key" | apt-key add -
salt-master:
    pkg.installed:
        - skip_verify: True
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/salt/master
            - file: /etc/salt/pki/master/master.pem
            - file: /etc/salt/pki/master/master.pub

/etc/salt/master:
    file.managed:
        - source: salt://files/etc/salt/master

/etc/salt/pki/master/master.pem:
    file.managed:
        - source: salt://files/etc/salt/pki/master/master.pem
        - mode: 600

/etc/salt/pki/master/master.pub:
    file.managed:
        - source: salt://files/etc/salt/pki/master/master.pub
        - mode: 644

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

udhcpd:
    pkg.purged

dnsmasq:
    pkg:
        - installed
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/dnsmasq.conf
    file.managed:
        - name: /etc/dnsmasq.conf
        - source: salt://files/etc/dnsmasq.conf
    require:
        - host: packmaster
        # watch hosts file??

hostapd:
    pkg:
        - installed
    service:
        - running
        - enable: True
        - watch:
            - file: /etc/hostapd/hostapd.conf
            - file: /etc/default/hostapd

vim:
    pkg.installed

bind9-host:
    pkg.installed

/etc/default/hostapd:
    file.managed:
        - source: salt://files/etc/default/hostapd

/etc/hostapd/hostapd.conf:
    file.managed:
        - source: salt://files/etc/hostapd/hostapd.conf

/etc/dhcp/dhclient.conf:
    file.managed:
        - source: salt://files/etc/dhcp/dhclient.conf

/root/.ssh/authorized_keys:
    file.managed:
        - source: salt://files/root/.ssh/authorized_keys

# networking
/etc/network/interfaces:
    file.managed:
        - source: salt://files/etc/network/interfaces

/etc/hostname:
    file.managed:
        - source: salt://files/etc/hostname

hostname:
    cmd.wait:
        - name: hostname -F /etc/hostname
        - watch:
            - file: /etc/hostname

/etc/init.d/masquerade:
    file.managed:
        - source: salt://files/etc/init.d/masquerade
        - mode: 755

net.ipv4.ip_forward:
    sysctl.present:
        - value: 1

masquerading:
    cmd.wait:
        - name: update-rc.d masquerade defaults; /etc/init.d/masquerade
        - watch:
            - file: /etc/init.d/masquerade

# needs dnsmasq restart
packmaster:
    host.present:
        - ip: 10.1.2.1
        - names:
            - salt
            - pm
            - packmaster

#/srv/salt:
#    file.recurse:
#        - source: salt://salt
#        - clean: True

#/srv/salt:
#    file:
#        - directory

/srv/salt/top.sls:
    file.managed:
        - source: salt://salt/top.sls

/srv/salt/wolfbot.sls:
    file.managed:
        - source: salt://salt/wolfbot.sls

# files.recurse broken in salt 17.4!
/srv/salt/_grains:
    file.recurse:
        - source: salt://salt/_grains
        - clean: True

/srv/salt/files:
    file.recurse:
        - source: salt://salt/files
        - clean: True


# vim: set syntax=yaml :
