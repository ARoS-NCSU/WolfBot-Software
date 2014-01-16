#!/bin/sh

echo Removing old cache files which may have stale configuration
rm -rf /tmp/salt
rm -rf /tmp/.salt

echo On failure, check...
echo "  msgpack-python is installed on target"
echo "  salt version >17.4 for files.recurse IOError fix (use development branch if necessary)"

#salt-ssh -ldebug -c saltconf 'bb_usb' state.sls packmaster
#salt-ssh -c saltconf 'bb_usb' state.sls packmaster

salt-ssh -c salt 'packmaster' state.sls packmaster

