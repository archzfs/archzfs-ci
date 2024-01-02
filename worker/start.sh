#!/bin/sh

systemd-machine-id-setup

# create a new worker
su -s /bin/sh buildbot -c "
cd /worker
/home/buildbot/.local/bin/buildbot-worker create-worker . master $WORKER_NAME At3iiquae3AeTaex3eoc
rm info/admin info/host
"

# use pacman cache
#echo 'Server = http://pacman-cache:8080/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist

# init build chroot
su -s /bin/sh buildbot -c "
sudo ccm64 c || sudo ccm64 u
sudo cp /etc/pacman.conf /scratch/.buildroot/root/etc/
sudo mkdir -p /scratch/.buildroot/root/repo
sudo chmod o+rw /scratch/.buildroot/root/repo
"

# start systemd (will start the buildbot worker)
exec /lib/systemd/systemd
