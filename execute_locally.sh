#!/bin/sh

docker rm mexico

docker run --name mexico -v //D/MapPy_Imaging/spfeasZonal:/mnt/work/input spfeas_zonal:0.2.6
docker run --name mexico --mount source=//D/MapPy_Imaging/spfeasZonal,target=/mnt/work/input spfeas_zonal:0.2.6

mkdir temp

docker cp mexico:/mnt/work/output temp