#!/bin/bash
docker run --rm -d \
    --name pg-docker \
    -e POSTGRES_USER=ubuntu \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_DB=evs \
    -p 5432:5432 \
    -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data \
    postgres:9.5
