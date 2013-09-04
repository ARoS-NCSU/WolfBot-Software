#!/bin/sh

route add default gw 192.168.7.1
echo "nameserver 8.8.8.8" > /etc/resolv.conf

export DEBIAN_FRONTEND=noninteractive
apt-get install hostapd
apt-get insall salt-master
apt-get -y -o Dpkg::Options::="--force-confold" install ntp

apt-get -y install bind9-host
apt-get -y install vim
apt-get -y install ipython

# use the timezone we set in /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

depmod -a


