#!/bin/bash

echo "Updating packmaster filesystem"
rsync -vr fs/* packmaster:/

echo "Updating salt files"
rsync -vaL --exclude .git --delete ../salt packmaster:/srv/
