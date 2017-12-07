#!/bin/bash

#
# Push packages to remote repository using sshfs
#

REMOTE_SERVER=$1
REMOTE_PATH=$2

# only continue, if inside a container
if [[ ! -f /.dockerenv ]]; then
    echo 'Not running inside docker!'
    exit 1
fi

function cleanup {
    sudo umount /data/pacman/repo
}
trap cleanup EXIT

# change repo name
sed -i 's/repo_basename="archzfs"/repo_basename="archzfs-ci"/' conf.sh

# add gpg key to config
key=$(gpg --list-keys --with-colons | awk -F: '/^pub:/ { print $5 }')
sed -i "s/gpg_sign_key='0EE7A126'/gpg_sign_key='${key}'/" conf.sh

# mount remote repo and add packages
sudo mkdir -p /data/pacman/repo
sudo chown buildbot:buildbot /data/pacman/repo
ssh "${REMOTE_SERVER}" echo 'can connect to repo server!'    && \
sshfs "${REMOTE_SERVER}:${REMOTE_PATH}" /data/pacman/repo -C && \
mkdir -p /data/pacman/repo/{archzfs-ci,archzfs-ci-archive}   && \
./repo.sh all azfs
