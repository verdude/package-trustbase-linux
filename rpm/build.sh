#!/bin/bash

VERSION=0.1.0
NAME=trustbase-linux
OWNER=verdude
RELEASE_NUMBER=27

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which dnf)" ]; then
    sudo dnf install -y fedora-packager fedora-review git gcc openssl-devel libconfig-devel libnl3-devel libsqlite3x-devel libcap-devel python-devel libevent-devel pyOpenSSL
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

rm -rf x86_64
rm -f *.rpm
./dl.sh $OWNER $NAME $VERSION

sudo fedpkg --release f$RELEASE_NUMBER local
exit_code=$?

rm $NAME-$VERSION.tar.gz
sudo rm -rf $NAME-$VERSION

if [ -d x86_64 ]; then
    sudo chown -R $USER:$USER x86_64
    sudo chown $USER:$USER *src.rpm
fi

exit $exit_code

