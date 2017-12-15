FROM debian:stretch
MAINTAINER minextu

# install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-psycopg2 \
                       libffi-dev libcairo2

# build master
RUN pip3 install 'buildbot[bundle]' && \
    pip3 install txrequests         && \
    pip3 install buildbot_pkg       && \
    pip3 install buildbot-badges

# add user and directory
RUN groupadd -r buildbot            && \
    useradd -r -g buildbot buildbot && \
    mkdir -p /master                && \
    chown -R buildbot:buildbot /master

# create buildbot master
USER buildbot
WORKDIR /master
RUN buildbot create-master .

# copy master.cfg
ADD master.cfg /master/
USER root
RUN chown buildbot:buildbot master.cfg
USER buildbot
RUN buildbot checkconfig master.cfg

ADD start.sh /
CMD ["sh", "/start.sh"]
