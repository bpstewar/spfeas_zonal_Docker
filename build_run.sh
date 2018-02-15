#!/bin/sh

docker build --tag spfeas_zonal:0.2.6 -f Dockerfile .

docker run -it spfeas_zonal:0.2.6