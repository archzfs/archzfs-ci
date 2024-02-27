FROM archlinux:base-devel
STOPSIGNAL SIGRTMIN+3

RUN pacman -Syu --noconfirm --needed python-pipx python-twisted python-future git wget systemd-sysvcompat openresolv vi btrfs-progs

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
# use custom pacman conf from devtools as archlinux image pacman.conf has NoExtract rules which interfere with builds
USER buildbot
RUN sudo ccm64 p                      && \
    echo 'CUSTOM_PACMAN_CONF="/usr/share/devtools/pacman.conf.d/extra.conf"' >> ~/.config/clean-chroot-manager.conf && \
    sudo mkdir -p /scratch/.buildroot

# set git directories to be safe (workaround for https://github.com/actions/checkout/issues/760) 
USER root
RUN git config --global --add safe.directory /worker/all/build/packages/dkms/zfs-dkms-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux-hardened/zfs-linux-hardened-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux-lts/zfs-linux-lts-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux/zfs-linux-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/linux-zen/zfs-linux-zen-git/zfs
RUN git config --global --add safe.directory /worker/all/build/packages/_utils/zfs-utils-git/zfs

# add nspawn wrapper to keep existing unit
USER root
COPY systemd-nspawn-wrapper /usr/local/bin/systemd-nspawn
RUN systemd-machine-id-setup

ADD start.sh /
CMD ["su", "-c", "sh /start.sh", "buildbot"]

