FROM archlinux/base
MAINTAINER minextu

RUN pacman -Syu --noconfirm --needed python-pip python-twisted python-future git wget base-devel systemd-sysvcompat openresolv vi

# install buildbot worker
RUN pip install buildbot-worker

# add buildbot user and give passwordless sudo access (needed for archzfs build scripts)
RUN groupadd -r buildbot && \
    useradd -m -g buildbot buildbot && \
    mkdir /worker && \
    chown buildbot:buildbot /worker && \
    echo "buildbot ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# aur prep
RUN useradd aur && \
    echo "aur ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers  && \
    sed -i '/en_US\.UTF-8 UTF-8/s/^#//' /etc/locale.gen && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf          && \
    locale-gen

# clean-chroot-manager
COPY ccm-PKGBUILD /tmp/ccm/PKGBUILD
USER aur
RUN cd /tmp/ccm && sudo chown aur:aur .  && \
    makepkg -si --noconfirm              && \
    rm -r /tmp/*

# run ccm64 once to generate config file
USER buildbot
RUN sudo ccm64                      && \
    sudo mkdir -p /scratch/.chroot64

# copy config file and set permissions
USER root
COPY clean-chroot-manager.conf /home/buildbot/.config/clean-chroot-manager.conf
RUN mkdir -p /scratch/.chroot64 && \
    chown buildbot:buildbot /home/buildbot/.config/clean-chroot-manager.conf

# setup systemd to only start the buildbot worker
ADD buildbot-worker.service /etc/systemd/system/
ADD worker.target /etc/systemd/system/
RUN systemctl set-default worker.target

ADD start.sh /
VOLUME [ "/sys/fs/cgroup" ]
CMD ["sh", "/start.sh"]
