#!/bin/bash

OWNER=${1:-markoneill}
NAME=${2:-trustbase-linux}
VERSION=${3:-0.1.0}
LOCAL_INSTALL_DIR=build

git clone https://github.com/$OWNER/$NAME
mv $NAME $NAME-$VERSION

cd $NAME-$VERSION
# initialize sslsplit git submodule
git submodule init
git submodule update
cd ..

# Add the dkms.conf file to the source
cp dkms.conf $NAME-$VERSION
# change the install directory prefix from /usr/lib/trustbase-linux to $LOCAL_INSTALL_DIR
sed -i "s/^PREFIX = \S*$/PREFIX = $LOCAL_INSTALL_DIR/g" $NAME-$VERSION/Makefile
chmod 775 $NAME-$VERSION/policy-engine/plugins/*.py

tar cf $NAME-$VERSION.tar.gz $NAME-$VERSION
sudo rm -rf $NAME-$VERSION
