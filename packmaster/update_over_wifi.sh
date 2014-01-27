#!/bin/sh

echo Removing old cache files which may have stale configuration
rm -rf /tmp/salt
rm -rf /tmp/.salt

echo On failure IOError, check...
echo " - salt version >17.4 (use development branch if necessary)"
echo " - try removing /tmp/.salt on target"

#salt-ssh -ldebug -c saltconf 'bb_usb' state.sls packmaster
#salt-ssh -c saltconf 'bb_usb' state.sls packmaster

salt-ssh -c salt 'packmaster' state.sls packmaster

