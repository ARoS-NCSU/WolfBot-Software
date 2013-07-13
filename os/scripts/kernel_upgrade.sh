#!/bin/sh

VER=v3.8.13-bone22

rm -f install-me.sh
wget http://rcn-ee.net/deb/wheezy-armhf/${VER}/install-me.sh
chmod 755 install-me.sh
./install-me.sh
rm -f install-me.sh

