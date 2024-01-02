FROM archlinux:base-devel
STOPSIGNAL SIGRTMIN+3

RUN pacman -Syu --noconfirm --needed python-pipx python-twisted python-future git wget systemd-sysvcompat openresolv vi

# add buildbot user and give passwordless sudo access (needed for archzfs build scripts)
RUN groupadd -r buildbot && \
    useradd -m -g buildbot buildbot && \
    mkdir /worker && \
    chown buildbot:buildbot /worker && \
    echo "buildbot ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# aur prep
RUN useradd aur && \
    echo "aur ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# clean-chroot-manager
USER aur
RUN cd /tmp && \
    wget https://aur.archlinux.org/cgit/aur.git/snapshot/clean-chroot-manager.tar.gz && \
    tar -xvf clean-chroot-manager.tar.gz && \
    cd clean-chroot-manager              && \
    makepkg -si --noconfirm              && \
    rm -r /tmp/*

# install buildbot worker
USER buildbot
RUN pipx install buildbot-worker

# run ccm64 once to generate config file
USER buildbot
RUN sudo ccm64 p                      && \
    sudo mkdir -p /scratch/.buildroot

# set git directories to be safe (workaround for https://github.com/actions/checkout/issues/760) 
USER root
RUN git config --global --add safe.directory /worker/all/build/packages/dkms/zfs-dkms-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux-hardened/zfs-linux-hardened-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux-lts/zfs-linux-lts-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux/zfs-linux-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux-zen/zfs-linux-zen-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/_utils/zfs-utils-git/zfs

# setup systemd to only start the buildbot worker
USER root
ADD buildbot-worker.service /etc/systemd/system/
ADD worker.target /etc/systemd/system/
RUN systemctl set-default worker.target

ADD start.sh /
CMD ["sh", "/start.sh"]
