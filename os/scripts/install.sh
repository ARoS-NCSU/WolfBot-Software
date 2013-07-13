#!/bin/sh

# route through USB connected host
route add default gw 192.168.7.1
echo "nameserver 8.8.8.8" > /etc/resolv.conf

#apt-get update
apt-get install deb-multimedia-keyring
apt-get -y install ntp
#apt-get -y install bind9-host
apt-get -y install vim

# use the timezone we set in /etc/timezone
dpkg-reconfigure -f noninteractive tzdata

# let modprobe find wifi module
depmod -a

ROOT_UUID=$(blkid -t LABEL=rootfs -o value -s UUID)
sed 's/{{ROOT_UUID}}/'$ROOT_UUID'/' /boot/uboot/uEnv_template.txt > /boot/uboot/uEnv.txt

# moved to fstab.d
#echo "nodev /sys/kernel/debug    debugfs   defaults   0  0" >> /etc/fstab

update-rc.d wolfbot defaults
