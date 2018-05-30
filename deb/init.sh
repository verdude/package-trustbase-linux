#!/bin/bash

VERSION=0.1.0
ARCH=x86_64
NAME=trustbase-linux
OWNER=verdude
WHOAMI="Santiago Verdu santiagoverdu01@gmail.com"
UPSTREAM=http://santi.space

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which apt-get)" ]; then
    sudo apt-get update
    sudo apt-get install -y linux-headers-$(uname -r) dkms debhelper pkg-config libssl-dev libevent-dev libconfig-dev libsqlite3-dev libcap-dev libnl-genl-3-dev python2.7-dev alien
else
    echo "This script is meant to be run on debian/ubuntu."
    exit 1
fi

rm -rf trust*

git clone https://github.com/$OWNER/$NAME
mv $NAME $NAME-$VERSION
cp -r debian $NAME-$VERSION

# make ubuntu compatible
sed -i 's/#include <linux\/sched\/signal.h>/#include <linux\/signal.h>/g' $NAME-$VERSION/loader.c

# dkms
cp dkms.conf $NAME-$VERSION

