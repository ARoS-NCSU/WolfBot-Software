#!/bin/sh

ip=${1:-192.168.7.2}
rsync -vtr fs scripts root@$ip:
rsync -vtr --delete ../agent ../config ../setup ../util root@$ip:/wolfbot/

