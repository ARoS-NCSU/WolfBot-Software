#!/bin/sh

# one time networking setup
route add default gw 192.168.7.1
echo "nameserver 8.8.8.8" > /etc/resolv.conf

wget -q -O- "http://debian.saltstack.com/debian-salt-team-joehealy.gpg.key" | apt-key add -
apt-get update

export DEBIAN_FRONTEND=noninteractive
apt-get purge udhcpd
apt-get install hostapd dnsmasq
apt-get -y -o Dpkg::Options::="--force-confold" install ntp

apt-get install salt-master

apt-get -y install bind9-host
apt-get -y install vim
apt-get -y install ipython

# use the timezone we set in /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

depmod -a

update-rc.d masquerade defaults
