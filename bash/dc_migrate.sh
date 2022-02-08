#!/bin/bash

cd "$1" || return 0

docker-compose exec -T php-fpm /app/vendor/bin/hidev migrate/up yes