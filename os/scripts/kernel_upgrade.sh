#!/bin/bash

VER=3.8.13-bone22

if [ $VER == `uname -r` ] ; then
  echo Kernel already upgraded
else
  rm -f install-me.sh
  wget http://rcn-ee.net/deb/wheezy-armhf/v${VER}/install-me.sh
  chmod 755 install-me.sh
  ./install-me.sh
  rm -f install-me.sh
  if [ "$1"x == "-r"x ] ; then
    reboot
  fi
fi

