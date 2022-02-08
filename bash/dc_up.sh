#!/bin/bash

cd "$1" || return 0

docker-compose up -d &> /dev/null
