#!/bin/sh

sudo rm -rf ./temp

# docker build --tag spfeas_zonal:0.2.6 -f Dockerfile .

docker-compose up --build 

