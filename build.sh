#!/bin/bash
script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# build archzfs-ci master and worker docker images
docker build -t archzfs-master ${script_dir}/docker/master && \
docker build -t archzfs-worker ${script_dir}/docker/worker
