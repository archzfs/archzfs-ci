#!/bin/sh
DOCKER_SOCKET=/var/run/docker.sock
DOCKER_GROUP=docker
REGULAR_USER=buildbot
MASTER=`pwd`

# give builbot permission to use docker
if [ -S ${DOCKER_SOCKET} ]; then
    DOCKER_GID=$(stat -c '%g' ${DOCKER_SOCKET})
    groupadd -for -g ${DOCKER_GID} ${DOCKER_GROUP}
    usermod -aG ${DOCKER_GROUP} ${REGULAR_USER}
fi

# Change to regular user
su ${REGULAR_USER} -c "

# remove any previous pid
rm -f ${MASTER}/twistd.pid

# upgrade database
until buildbot upgrade-master ${MASTER}
do
    echo \"Can't upgrade master yet. Waiting for database to be ready...\"
    sleep 1
done

# use exec so that twistd will use pid 1 of the container, and signals are properly forwarded
exec twistd -ny ${MASTER}/buildbot.tac

"
