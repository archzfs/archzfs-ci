#!/bin/sh

# create a new worker
su -s /bin/sh buildbot -c "
cd /worker
buildbot-worker create-worker . master '$WORKERNAME' '$WORKERPASS'
rm info/admin info/host
"

# start systemd (will start the buildbot worker)
exec /usr/bin/init
