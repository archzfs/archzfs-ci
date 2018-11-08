FROM base/devel
MAINTAINER minextu

# install nginx
RUN pacman -Sy --noconfirm nginx pacman-contrib && \
    find /var/cache/pacman/pkg -mindepth 1 -delete

# setup nginx
ADD nginx.conf /etc/nginx/
RUN mkdir -p /srv/http/pacman-cache         && \
    chown http:http /srv/http/pacman-cache

ADD start.sh /
CMD ["sh", "/start.sh"]
