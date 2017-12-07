#!/bin/bash

errors=false
if [[ ! -f /worker/secrets/ssh_key ]]; then
    echo 'deploy/secrets/ssh_key missing'
    errors=true
fi
if [[ ! -f /worker/secrets/ssh_server_hostkeys ]]; then
    echo 'deploy/secrets/ssh_server_hostkeys missing'
    errors=true
fi
if [[ ! -f /worker/secrets/gpg_key ]]; then
    echo 'deploy/secrets/gpg_key missing'
    errors=true
fi

if [ "${errors}"  = true ]; then
    echo 'Not starting deploy container due to errors!'
    exit 1
fi

# add ssh key
mkdir -p /home/buildbot/.ssh
cp /worker/secrets/ssh_key /home/buildbot/.ssh/id_rsa
cp /worker/secrets/ssh_server_hostkeys /home/buildbot/.ssh/known_hosts
chown -R buildbot:buildbot /home/buildbot/.ssh && \
chmod -R go-rwx /home/buildbot/.ssh

# add gpg key
mkdir -p /home/buildbot/.gpg
cp /worker/secrets/gpg_key /home/buildbot/.gpg/gpg_key
chown -R buildbot:buildbot /home/buildbot/.gpg && \
chmod -R go-rwx /home/buildbot/.gpg
su -s /bin/sh buildbot -c "
gpg --import ~/.gpg/gpg_key
"

# start this worker
exec /start.sh
