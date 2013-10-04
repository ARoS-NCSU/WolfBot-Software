#!/bin/sh

# Questions: 
#  - best way to run this from packmaster?
#  - should we bootstrap immediately after image install (no reboot)?
#      - copy salt pkgs and bootstrap state over?
#  - salt bootstrap role?

# need to check mac address

ip=${1:-192.168.7.2}

rsync -rv ../salt/files/root/.ssh root@$ip:/root/
#rsync -v ../salt/files/etc/wpa_supplicant.conf root@$ip:/etc
#rsync -v ../salt/files/etc/network/interfaces root@$ip:/etc/network
rsync -rv salt_pkgs root@$ip:/root/
rsync -v salt_bootstrap_local.sh root@$ip:/root/
#ssh root@$ip salt_bootstrap_local.sh
#ssh root@$ip "rm -rf salt_bootstrap_local.sh"

