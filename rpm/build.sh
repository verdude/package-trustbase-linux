#!/bin/bash

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which dnf)" ]; then
    sudo dnf install fedora-packager fedora-review git
else
    echo "This script is meant to be run on Fedora."
    exit
fi

id $USER | grep -q mock
in_mock_group=$?
if [ "$in_mock_group" -ne 0 ]; then
    # add the user to the mock group
    sudo usermod -a -G mock $USER
    newgrp
fi

mkdir git
git clone https://github.com/markoneill/trustbase-linux git/trustbase-linux
tar cf trustbase-1.0.0.tar.gz git/trustbase-linux

sudo fedpkg --release f27 local

