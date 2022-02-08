#!/bin/bash

cd "$1" || return 0

docker-compose down &> /dev/null
