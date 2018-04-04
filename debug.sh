#!/bin/bash

docker-compose build

docker-compose run --service-ports spfeas_zonal
