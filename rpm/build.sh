#!/bin/bash

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which dnf)" ]; then
    sudo dnf install fedora-packager fedora-review git
    sudo dnf install openssl-devel libconfig-devel libnl3-devel libsqlite3x-devel libcap-devel python-devel libevent-devel pyOpenSSL
    sudo yum install kernel-devel-$(uname -r) kernel-headers-$(uname -r)
else
    echo "This script is meant to be run on Fedora."
    exit 1
fi

exit
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

mkdir git
git clone https://github.com/markoneill/trustbase-linux git/trustbase-linux
# change the build target to a local directory
sed 's/^PREFIX = \S*$/PREFIX = build/g' git/trustbase-linux/Makefile > git/trustbase-linux/Makefile
tar cf trustbase-1.0.0.tar.gz git/trustbase-linux

sudo fedpkg --release f27 local

