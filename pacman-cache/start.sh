#!/bin/bash

# remove old packages
find /srv/http/pacman-cache/ -type d -exec paccache -v -r -k 1 -c {} \;

# fix permissions
chown -R http:http /srv/http/pacman-cache

# start nginx
/usr/bin/nginx -g "daemon off;"
