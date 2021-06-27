FROM archlinux:base-devel
STOPSIGNAL SIGRTMIN+3

RUN pacman -Syu --noconfirm --needed python-pip python-twisted python-future git wget systemd-sysvcompat openresolv vi

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
    echo "aur ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# clean-chroot-manager
USER aur
RUN cd /tmp && \
    wget https://aur.archlinux.org/cgit/aur.git/snapshot/clean-chroot-manager.tar.gz && \
    tar -xvf clean-chroot-manager.tar.gz && \
    cd clean-chroot-manager              && \
    makepkg -si --noconfirm              && \
    rm -r /tmp/*

# run ccm64 once to generate config file
USER buildbot
RUN sudo ccm64 p                      && \
    sudo mkdir -p /scratch/.buildroot

# setup systemd to only start the buildbot worker
USER root
ADD buildbot-worker.service /etc/systemd/system/
ADD worker.target /etc/systemd/system/
RUN systemctl set-default worker.target

ADD start.sh /
CMD ["sh", "/start.sh"]
