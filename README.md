# Mycelium
Destributed system
 
# MASTER

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

# NODE

docker build \
    --rm \
    --tag=mycelium-node:latest \
    ./node/ ;\
docker run \
    -it \
    --rm \
    -p 5001:5000 \
    --name myc-n \
    mycelium-node:latest