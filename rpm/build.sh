#!/bin/bash

VERSION=1.0.0
NAME=trustbase-linux
OWNER=verdude

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which dnf)" ]; then
    sudo dnf install -y fedora-packager fedora-review git gcc
else
    echo "This script is meant to be run on Fedora."
    exit 1
fi

if [ -z "$(id $USER | grep mock)" ]; then
    # add the user to the mock group
    echo "adding $USER to group mock"
    sudo usermod -a -G mock $USER
    newgrp
    # check if adding to group succeeded.
    id $USER | grep -q mock
    if [ "$?" -ne 0 ]; then
        echo "Error adding $USER to mock group"
        exit 1
    fi
fi

rm -rf x86_64/$NAME-$VERSION*.rpm
rm -f *.rpm
git clone https://github.com/$OWNER/$NAME
mv $NAME $NAME-$VERSION
tar cf $NAME-$VERSION.tar.gz $NAME-$VERSION
sudo rm -rf $NAME-$VERSION

sudo fedpkg --release f27 local
exit_code=$?

rm $NAME-$VERSION.tar.gz
sudo rm -rf $NAME-$VERSION

if [ -d x86_64 ]; then
    sudo chown -R $USER:$USER x86_64
fi

exit $exit_code

