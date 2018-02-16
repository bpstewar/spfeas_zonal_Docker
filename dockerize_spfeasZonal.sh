#!/bin/sh

docker build --tag spfeas_zonal:0.2.6 -f Dockerfile .

docker login

docker tag spfeas_zonal:0.2.6 geographyis/spfeas_zonal:latest

docker push geographyis/spfeas_zonal:latest

