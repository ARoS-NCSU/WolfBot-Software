#!/bin/sh

# route through USB connected host
route add default gw 192.168.7.1
echo "nameserver 8.8.8.8" > /etc/resolv.conf

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y install salt-minion
apt-get -y install locales
dpkg-reconfigure -f noninteractive locales 

apt-get -y -o Dpkg::Options::="--force-confold" install ntp
apt-get -y --force-yes install deb-multimedia-keyring
apt-get update
apt-get -y -o Dpkg::Options::="--force-confold" install ffmpeg

apt-get -y install bind9-host
apt-get -y install vim
apt-get -y install ipython

# wolfbot code dependencies
apt-get -y install python-yaml python-smbus

# use the timezone we set in /etc/timezone
dpkg-reconfigure -f noninteractive tzdata


# let modprobe find wifi module
depmod -a

ROOT_UUID=$(blkid -t LABEL=rootfs -o value -s UUID)
sed 's/{{ROOT_UUID}}/'$ROOT_UUID'/' /boot/uboot/uEnv_template.txt > /boot/uboot/uEnv.txt

# moved to fstab.d
#echo "nodev /sys/kernel/debug    debugfs   defaults   0  0" >> /etc/fstab

update-rc.d wolfbot defaults

touch /wolfbot/.install_timestamp
