#!/bin/bash
docker build -t archzfs-master master/  && \
docker build -t archzfs-worker worker/  && \
docker-compose up

