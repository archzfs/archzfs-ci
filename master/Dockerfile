FROM debian:stretch
MAINTAINER minextu

# install dependencies
RUN apt-get update && \
    apt-get install -y python python-dev python-pip python-psycopg2

# upgrade pip
RUN pip install --upgrade pip

# build master
RUN pip install 'buildbot[bundle]'

# add user and directory
RUN groupadd -r buildbot && \
    useradd -r -g buildbot buildbot && \
    mkdir /master && \
    chown buildbot:buildbot /master

# create buildbot master
USER buildbot
WORKDIR /master
RUN buildbot create-master .

# use buildbot logs for output
USER root
RUN ln -s /master/twisted.log /dev/stdio

# copy master.cfg
ADD master.cfg /master/
RUN chown buildbot:buildbot master.cfg
USER buildbot
RUN buildbot checkconfig master.cfg

ADD start.sh /
CMD ["sh", "/start.sh"]
