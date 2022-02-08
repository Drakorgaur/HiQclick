#!/bin/bash

docker run -d -p 80:80 --rm --network nginx-proxy-network-127.0.0.2 -v \
/var/run/docker.sock:/tmp/docker.sock:ro jwilder/nginx-proxy
