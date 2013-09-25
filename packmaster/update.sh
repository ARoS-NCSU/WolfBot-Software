#!/bin/bash

echo "Updating packmaster filesystem"
rsync -vr fs/* packmaster:/

echo "Updating salt files"
rsync -vaL --delete ../salt packmaster:/srv/
