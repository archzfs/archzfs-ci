FROM debian:bullseye

# install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python3-psycopg2 python3-pil \
                       # needed for buildbot badges
                       libffi-dev libcairo2                             \
                       # email tls support
                       python3-openssl python3-service-identity         \
                       # rust + cryptography
                       curl libssl-dev                                  \
                       git 

# update outdated dependencies
RUN pip3 install --upgrade six cairocffi attrs service_identity pyOpenSSL

# build master
RUN pip3 install 'buildbot[bundle]' && \
    # github api support
    pip3 install txrequests         && \
    # needed for badges
    pip3 install buildbot_pkg       && \
    pip3 install buildbot-badges    && \
    # update outdated dependencies
    pip3 install --upgrade six cairocffi attrs service_identity

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
