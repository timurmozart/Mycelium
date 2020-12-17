#!/bin/bash

sudo docker build --rm --tag mycelium-secondary:krystina .
cd ../../..
sudo docker run -it --rm -p 8001:8001 -p 8011 --name myc-n2 --hostname myc-n2 --network myc-network mycelium-secondary:krystina
