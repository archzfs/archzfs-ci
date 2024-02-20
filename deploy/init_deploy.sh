#!/bin/bash

# only continue, if inside a container
if [[ ! -f /.dockerenv ]]; then
    echo 'Not running inside docker!'
    exit 1
fi

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

# init git config
su buildbot <<EOF
git config --global user.name "Archzfs Buildbot"
git config --global user.email "$GIT_EMAIL"
EOF

# gpg
rm -rf /home/buildbot/.gnupg
mkdir -p /home/buildbot/.gnupg
cp /worker/secrets/gpg_key /home/buildbot/.gnupg/gpg_key
chown -R buildbot:buildbot /home/buildbot/.gnupg
chmod -R go-rwx /home/buildbot/.gnupg

# import gpg secret key and remove passphrase
su buildbot <<EOF
gpg-agent --daemon
gpg --batch --import ~/.gnupg/gpg_key
key=\$(gpg --list-secret-keys --with-colons | awk -F: '/^sec:/ { print \$5 }')

# remove gpg passphrase
/usr/bin/expect <<EOD
spawn bash -c "gpg --pinentry-mode loopback --batch --command-fd 0 --status-fd 2 --change-passphrase \$key"
expect "*?passphrase.enter"
log_user 0
send "$GPG_PASSPHRASE\r"
expect "*?passphrase.enter"
log_user 1
send "\r"
expect "*?passphrase.enter"
send "\r"
expect eof
EOD

# trust key
expect -c "spawn gpg --edit-key \$key trust quit; send \"5\ry\r\"; expect eof"
EOF

# start this worker with clean environment variables
exec /bin/env -i WORKER_NAME=${WORKER_NAME} PATH={$PATH} su -c "sh /start.sh" buildbot