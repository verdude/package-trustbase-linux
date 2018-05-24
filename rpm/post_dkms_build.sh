#!/bin/sh

cd /var/lib/dkms/trustbase-linux/1.0.0/build
if [ -d /usr/lib64/trustbase-linux ]; then
    cp modules.order /usr/lib64/trustbase-linux  >> $out 2>&1
    cp Module.symvers /usr/lib64/trustbase-linux  >> $out 2>&1
elif [ -d /usr/lib/trustbase-linux ]; then
    cp modules.order /usr/lib/trustbase-linux  >> $out 2>&1
    cp Module.symvers /usr/lib/trustbase-linux  >> $out 2>&1
fi

