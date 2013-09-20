#!/bin/bash

# TODO: need a one-time script to depmod -a on first boot

image=$1
device=$2

if [ ! -f $image ]; then
    echo "Can't find image file: $2"
    exit 1
fi

if [ x$device == x ]; then
    echo "Need to specify device (sdX)"
    exit 1
fi

dd if=$image of=/dev/$device bs=1M

mount /dev/${device}2 /mnt/
if [ $? -ne 0 ]; then
    echo "Failed to mount /dev/${device}2"
    exit 1
fi

grep -q arm /mnt/etc/hostname
if [ $? -eq 1 ]; then
    echo "Not a valid image!"
    umount /mnt/
    exit 1
fi


rsync -vr ../salt/files/root/.ssh /mnt/root/
chown -R root.root /mnt/root/.ssh
rsync -v ../salt/files/etc/wpa_supplicant.conf /mnt/etc
rsync -rv ../salt/files/etc/modprobe.d /mnt/etc
rsync -rv ../salt/files/lib/modules /mnt/lib/
rsync -v ../salt/files/etc/network/interfaces /mnt/etc/network

rsync -rv salt_pkgs /mnt/root/

grep -q 8192 /mnt/etc/modules
if [ $? -eq 1 ]; then
    echo 8192cu >> /mnt/etc/modules
fi

umount /mnt/

