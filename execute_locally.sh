#!/bin/sh

rm -rf ./temp

docker build --tag spfeas_zonal:0.2.6 -f Dockerfile .

docker rm mexico

# docker run --name mexico -v //D/MapPy_Imaging/spfeasZonal:/mnt/work/input spfeas_zonal:0.2.6
# docker run --name mexico --mount source=//D/MapPy_Imaging/spfeasZonal,target=/mnt/work/input spfeas_zonal:0.2.6
docker run --name mexico -v $(pwd):/mnt/work/input/ spfeas_zonal:0.2.6

mkdir temp

docker cp mexico:/mnt/work/output temp
