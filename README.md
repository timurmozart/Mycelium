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
    --hostname=myc-m \
    --network=myc \
    mycelium-master:latest

# NODE

docker build \
    --rm \
    --tag=mycelium-node:latest \
    ./node/ ;\
docker run \
    -it \
    --rm \
    --hostname=myc-n \
    -p 8000/tcp \
    --name myc-n \
    --network=myc \
    mycelium-node:latest