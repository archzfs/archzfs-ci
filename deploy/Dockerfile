FROM archzfs-worker
MAINTAINER minextu

RUN pacman -Sy --noconfirm expect archiso

# copy secrets
ADD secrets/* /worker/secrets/
RUN chown -R buildbot:buildbot /worker/secrets && \
    chmod -R go-rwx /worker/secrets

# copy scripts
ADD prepare-workdir.sh /worker/

ADD init_deploy.sh /
CMD ["sh", "/init_deploy.sh"]
