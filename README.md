# Mycelium
Destributed system UCU 

-------------------------------------------------------------------------
### HTTP requests examples
**POST**  
`POST    localhost:8080/append`

body (JSON): 
`{
    "msg": "msg0",
    "write_concern": 1
}`  

**GET**  
`GET     localhost:8080/list`

-------------------------------------------------------------------------
### How to execute

`docker network create myc-network`

**Masret-node**  
* `cd app_final/dockerfiles/master`
* `docker build --rm --tag mycelium-master:krystina .`
* `cd ../../..`
* `docker  run \
        -it \
        --rm \
        -p 8080:8080 \
        --name myc-m \
        --hostname myc-m \
        --network myc-network \
        mycelium-master:krystina`  

**Secondary node 1**  
* `cd app_final/dockerfiles/secondary`
* `docker build --rm --tag mycelium-secondary:krystina .`
* `cd ../../..`
* `docker  run \
        -it \
        --rm \
        -p 8003:8003 \
        -p 8013 \
        --name myc-n1 \
        --hostname myc-n1 \
        --network myc-network \
        mycelium-secondary:krystina`  

**Secondary node 2**  
* `cd app_final/dockerfiles/secondary`
* `docker build --rm --tag mycelium-secondary:krystina .`
* `cd ../../..`
* `docker  run \
        -it \
        --rm \
        -p 8001:8001 \
        -p 8011 \
        --name myc-n2 \
        --hostname myc-n2 \
        --network myc-network \
        mycelium-secondary:krystina`  
