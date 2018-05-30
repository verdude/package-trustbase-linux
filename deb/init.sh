#!/bin/bash

VERSION=0.1.0
NAME=trustbase-linux
OWNER=verdude
WHOAMI="Santiago Verdu santiagoverdu01@gmail.com"

scriptpath="$(cd "$(dirname "$0")"; pwd -P)"
cd "$scriptpath"

if [ -n "$(which apt-get)" ]; then
    sudo apt-get update
    sudo apt-get install -y linux-headers-$(uname -r) dkms debhelper pkg-config libssl-dev libevent-dev libconfig-dev libsqlite3-dev libcap-dev libnl-genl-3-dev python2.7-dev
else
    echo "This script is meant to be run on debian/ubuntu."
    exit 1
fi

rm -rf trust*
rm -rf build-area

# git
rm -rf $NAME-$VERSION
git clone https://github.com/$OWNER/$NAME
mv $NAME $NAME-$VERSION

# make ubuntu compatible
sed -i 's/#include <linux\/sched\/signal.h>/#include <linux\/signal.h>/g' $NAME-$VERSION/loader.c

# dkms
cp dkms.conf $NAME-$VERSION

# tar
rm -f $NAME-$VERSION.tar.gz
tar czf $NAME-$VERSION.tar.gz $NAME-$VERSION

# bazaar
bzr dh-make $NAME $VERSION $NAME-$VERSION.tar.gz
cd $NAME/debian
mv postinst.ex postinst
mv postrm.ex postrm
vim -p changelog control copyright README* rules postinst postrm

