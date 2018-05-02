#!/bin/sh

# create a new worker
su -s /bin/sh buildbot -c "
cd /worker
buildbot-worker create-worker . master $WORKER_NAME At3iiquae3AeTaex3eoc
rm info/admin info/host
"

# use pacman cache
echo 'Server = http://cache:8080/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist

# start systemd (will start the buildbot worker)
exec /usr/bin/init
