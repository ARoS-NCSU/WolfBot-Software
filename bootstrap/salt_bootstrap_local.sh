#!/bin/sh

# get on the wolfbot network
ifup wlan0

# prep the salt install, which needs dependencies
dpkg --unpack salt_pkgs/*

# pull in dependecies to finish install
apt-get update
apt-get -y -f install


