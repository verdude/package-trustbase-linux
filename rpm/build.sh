#!/bin/bash

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which dnf)" ]; then
    sudo dnf install fedora-packager fedora-review git gcc
    sudo dnf install openssl-devel libconfig-devel libnl3-devel libsqlite3x-devel libcap-devel python-devel libevent-devel pyOpenSSL
    sudo dnf install kernel-devel-$(uname -r) kernel-headers-$(uname -r)
else
    echo "This script is meant to be run on Fedora."
    exit 1
fi

id $USER | grep -q mock
in_mock_group=$?
if [ "$in_mock_group" -ne 0 ]; then
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

git clone https://github.com/markoneill/trustbase-linux
# change the build target to a local directory
sed -i.bak 's/^PREFIX = \S*$/PREFIX = build/g' trustbase-linux/Makefile
tar cf trustbase-linux-1.0.0.tar.gz trustbase-linux
sudo rm -rf trustbase-linux

sudo fedpkg --release f27 local

rm trustbase-linux-1.0.0.tar.gz
sudo rm -rf trustbase-linux

if [ -d x86_64 ]; then
    sudo chown -R $USER:$USER x86_64
fi
