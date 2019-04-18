FROM archlinux/base
MAINTAINER minextu

# install nginx
RUN pacman -Syu --noconfirm nginx pacman-contrib gawk

# setup nginx
ADD nginx.conf /etc/nginx/
RUN mkdir -p /srv/http/pacman-cache         && \
    chown http:http /srv/http/pacman-cache

ADD start.sh /
CMD ["sh", "/start.sh"]
