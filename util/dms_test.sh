#!/bin/sh

while :; do
    ./dms_select.sh 0 0 0
    ./dms_read.sh
    ./dms_select.sh 0 0 1
    ./dms_read.sh
    ./dms_select.sh 0 1 0
    ./dms_read.sh
    ./dms_select.sh 0 1 1
    ./dms_read.sh
    echo
done

