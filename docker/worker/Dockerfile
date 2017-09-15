FROM base/devel
MAINTAINER minextu

RUN pacman -Sy --noconfirm python2-pip python2-twisted python2-future && \
    find /var/cache/pacman/pkg -mindepth 1 -delete

# install buildbot worker
RUN pip2 install buildbot-worker

# add buildbot user and give passwordless sudo access (needed for archzfs build scripts)
RUN groupadd -r buildbot && \
    useradd -m -r -g buildbot buildbot && \
    mkdir /worker && \
    chown buildbot:buildbot /worker && \
    echo "buildbot ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

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
RUN pacman -Sy --noconfirm git pkgbuild-introspection wget && \
    find /var/cache/pacman/pkg -mindepth 1 -delete

# aur prep
RUN useradd aur && \
    echo "aur ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# clean-chroot-manager
USER aur
RUN cd /tmp && \
    wget https://aur.archlinux.org/cgit/aur.git/snapshot/clean-chroot-manager.tar.gz && \
    tar -xvf clean-chroot-manager.tar.gz && \
    cd clean-chroot-manager              && \
    makepkg -si --noconfirm

# run ccm64 once to generate config file
USER buildbot
RUN sudo ccm64                      && \
    sudo mkdir -p /scratch/chroot64

USER root
ADD start.sh /
VOLUME [ "/sys/fs/cgroup" ]
CMD ["sh", "/start.sh"]
