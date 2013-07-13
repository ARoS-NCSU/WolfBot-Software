#!/bin/sh

ip=${1:-192.168.7.2}
rsync -vr fs scripts root@$ip:

