#!/bin/bash

set -e
VERSION=1.0.0
NAME=trustbase-linux
OWNER=markoneill

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

git clone https://github.com/$OWNER/$NAME
# change the build target to a local directory
sed -i.bak 's/^PREFIX = \S*$/PREFIX = build/g' $NAME/Makefile
mv $NAME $NAME-$VERSION
cp dkms.conf $NAME-$VERSION
tar cf $NAME-$VERSION.tar.gz $NAME-$VERSION
sudo rm -rf $NAME-$VERSION

sudo fedpkg --release f27 local

rm $NAME-$VERSION.tar.gz
sudo rm -rf $NAME-$VERSION

if [ -d noarch ]; then
    sudo chown -R $USER:$USER noarch
fi
