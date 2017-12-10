FROM archzfs-worker
MAINTAINER minextu

# copy secrets
ADD secrets/* /worker/secrets/
RUN chown -R buildbot:buildbot /worker/secrets && \
    chmod -R go-rwx /worker/secrets

# copy push.sh
ADD update-config.sh /worker/

ADD init_deploy.sh /
CMD ["sh", "/init_deploy.sh"]
