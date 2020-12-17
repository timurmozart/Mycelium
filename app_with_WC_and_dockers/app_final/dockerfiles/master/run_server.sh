#!/bin/bash

sudo docker build --rm --tag mycelium-master:krystina .
cd ../../..
sudo docker run -it --rm -p 8080:8080 --name myc-m --hostname myc-m --network myc-network  mycelium-master:krystina