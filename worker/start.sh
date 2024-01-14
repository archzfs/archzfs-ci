#!/bin/sh

cd /worker
/home/buildbot/.local/bin/buildbot-worker create-worker . master $WORKER_NAME At3iiquae3AeTaex3eoc
rm info/admin info/host
rm -f /worker/twistd.pid
exec /home/buildbot/.local/bin/buildbot-worker start --nodaemon /worker

