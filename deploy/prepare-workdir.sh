#!/bin/bash

#
# Setup workdir for deployment
#

REMOTE_SERVER=$1
REMOTE_PATH=$2
REMOTE_REPO_BASENAME=$3

# only continue, if inside a container
if [[ ! -f /.dockerenv ]]; then
    echo 'Not running inside docker!'
    exit 1
fi

# reset config file
git checkout conf.sh

# change builduser
sed -i 's/demizer/buildbot/' conf.sh

# change repo name
sed -i "s/repo_basename=\"archzfs\"/repo_basename=\"${REMOTE_REPO_BASENAME}\"/" conf.sh

# update remote server
sed -i "s/remote_login=\"webfaction\"/remote_login=\"${REMOTE_SERVER}\"/" conf.sh
sed -i "s#repo_remote_basepath=\"/home/jalvarez/webapps/default\"#repo_remote_basepath=\"${REMOTE_PATH}\"#" conf.sh

# add gpg key to config
key=$(gpg --list-keys --with-colons | awk -F: '/^pub:/ { print $5 }')
sed -i "s/gpg_sign_key='0EE7A126'/gpg_sign_key='${key}'/" conf.sh

# create repo dir
sudo mkdir -p /data/pacman/repo
sudo chown buildbot:buildbot /data/pacman/repo
