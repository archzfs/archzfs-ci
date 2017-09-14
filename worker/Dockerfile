FROM base/devel
MAINTAINER minextu

RUN pacman -Sy --noconfirm python2-pip python2-twisted python2-future && \
    find /var/cache/pacman/pkg -mindepth 1 -delete

# install buildbot worker
RUN pip2 install buildbot-worker

# add buildbot user
RUN groupadd -r buildbot && \
    useradd -r -g buildbot buildbot && \
    mkdir /worker && \
    chown buildbot:buildbot /worker

# create a new worker
USER buildbot
WORKDIR /worker
RUN buildbot-worker create-worker . buildbot archzfs-worker At3iiquae3AeTaex3eoc

# remove all systemd services
USER root
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done) && \
rm -f /lib/systemd/system/multi-user.target.wants/*       && \
rm -f /etc/systemd/system/*.wants/*                       && \
rm -f /lib/systemd/system/local-fs.target.wants/*         && \
rm -f /lib/systemd/system/sockets.target.wants/*udev*     && \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*  && \
rm -f /lib/systemd/system/basic.target.wants/*            && \
rm -f /lib/systemd/system/anaconda.target.wants/*

# add buildbot systemd service
ADD buildbot-worker.service /etc/systemd/system/
RUN systemctl enable buildbot-worker.service

# install archzfs dependencies
RUN pacman -Sy --noconfirm git && \
    find /var/cache/pacman/pkg -mindepth 1 -delete

VOLUME [ "/sys/fs/cgroup" ]
CMD ["/usr/bin/init"]
