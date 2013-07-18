#!/bin/sh

ip=${1:-192.168.7.2}

./stage_files.sh $ip
ssh root@$ip scripts/copy_files.sh
ssh root@$ip scripts/install.sh
ssh root@$ip "scripts/kernel_upgrade.sh -r"

