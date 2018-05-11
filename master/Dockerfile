FROM debian:stretch
MAINTAINER minextu

# install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-psycopg2 \
                       # needed for buildbot badges
                       libffi-dev libcairo2                             \
                       # email tls support
                       python3-openssl python3-service-identity

# build master
RUN pip3 install 'buildbot[bundle]' && \
    # github api support
    pip3 install txrequests         && \
    # needed for badges
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
ADD config/* /master/
USER root
RUN chown buildbot:buildbot *
USER buildbot
RUN buildbot checkconfig master.cfg

ADD start.sh /
CMD ["sh", "/start.sh"]
