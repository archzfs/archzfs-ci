FROM base/devel
MAINTAINER minextu

RUN pacman -Sy --noconfirm python-pip python-twisted python-future git wget ccache aarch64-linux-gnu-gcc && \
    find /var/cache/pacman/pkg -mindepth 1 -delete

# install buildbot worker
RUN pip install buildbot-worker

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

# add buildbot user and give passwordless sudo access (needed for archzfs build scripts)
RUN groupadd -r buildbot && \
    useradd -m -r -g buildbot buildbot && \
    mkdir /worker && \
    chown buildbot:buildbot /worker && \
    echo "buildbot ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# aur prep
RUN useradd -m aur && \
    echo "aur ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers  && \
    sed -i '/en_US\.UTF-8 UTF-8/s/^#//' /etc/locale.gen && \
    echo "LANG=en_US.UTF-8" > /etc/locale.conf          && \
    locale-gen

# clean-chroot-manager
ADD clean-chroot-manager.conf /home/buildbot/.config/
RUN mkdir -p /scratch/{ccache,.chroot64} && \
    chown buildbot:buildbot /scratch/ccache
USER aur
RUN cd /tmp && \
    wget https://aur.archlinux.org/cgit/aur.git/snapshot/clean-chroot-manager.tar.gz && \
    tar -xvf clean-chroot-manager.tar.gz && \
    cd clean-chroot-manager              && \
    # patch for ccache, arm
    sed -i 's#^source=.*$#source=("https://github.com/minextu/clean-chroot-manager/archive/master.zip")#' PKGBUILD && \
    sed -i 's#^sha256sums=.*$#sha256sums=(SKIP)#' PKGBUILD && \
    sed -i 's#cd "$pkgname-$pkgver"#cd "$pkgname-master"#' PKGBUILD && \
    makepkg -si --noconfirm              && \
    rm -r /tmp/*

# aarch64-linux-gnu-libutil-linux
RUN cd /tmp && \
    gpg --recv-keys B0C64D14301CC6EFAEDF60E4E4B71D5EEC39C284 && \
    wget https://aur.archlinux.org/cgit/aur.git/snapshot/aarch64-linux-gnu-util-linux.tar.gz && \
    tar -xvf aarch64-linux-gnu-util-linux.tar.gz && \
    cd aarch64-linux-gnu-util-linux              && \
    makepkg -s --noconfirm                       && \
    sudo mkdir /packages                         && \
    sudo cp *.pkg.tar.xz /packages/              && \
    rm -r /tmp/*

USER root

# fix for https://github.com/systemd/systemd/issues/6347
RUN sed -i 's/--register=no/--register=no --machine \$(uuidgen)/' /usr/bin/arch-nspawn
# fix for https://bugs.archlinux.org/task/40946 (makechrootpkg never got patched)
ADD arm-setarch-fix.patch /root/
RUN patch -i /root/arm-setarch-fix.patch /usr/bin/makechrootpkg

ADD makepkg.conf.aarch64 /root/

ADD start.sh /
VOLUME [ "/sys/fs/cgroup" ]
CMD ["sh", "/start.sh"]
