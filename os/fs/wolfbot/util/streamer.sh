#!/bin/sh

pkill ffserver

ffserver

# moved to /etc/ffserver.conf, Launch param
#ffmpeg -f video4linux2 -vcodec mjpeg -r 5 -i /dev/video0 http://localhost:8090/feed1.ffm

