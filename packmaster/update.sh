#!/bin/bash

echo "Updating packmaster filesystem"
rsync -vr fs/* root@packmaster:/

echo "Updating salt files"
rsync -vaL --exclude .git --delete ../salt root@packmaster:/srv/
