#!/bin/bash
#Stop all containers
docker stop $(docker ps -aq)

# Delete volumes
docker volume rm $(docker volume ls -q -f dangling=true)

# Delete containers
docker rm $(docker ps -a -q)

# Delete images
docker rmi --force $(docker images -a -q)
