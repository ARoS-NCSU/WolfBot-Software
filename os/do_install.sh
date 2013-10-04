#!/bin/sh

ip=${1:-192.168.7.2}

rsync -rv fs/root/.ssh root@$ip:/root/
./stage_files.sh $ip
ssh root@$ip scripts/copy_files.sh
ssh root@$ip scripts/install.sh
ssh root@$ip "scripts/kernel_upgrade.sh -r"
ssh root@$ip "rm -rf fs scripts"

