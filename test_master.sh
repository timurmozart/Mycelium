#!/bin/bash
docker build \
    --rm \
    --tag=mycelium-master:latest \
    ./master/ ;\
docker run \
    -it \
    --rm \
    -p 5000:5000 \
    --name myc-m \
    mycelium-master:latest