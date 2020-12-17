#!/bin/bash

sudo docker build --rm --tag mycelium-secondary:krystina .
cd ../../..
sudo docker run -it --rm -p 8003:8003 -p 8013 --name myc-n1 --hostname myc-n1 --network myc-network mycelium-secondary:krystina