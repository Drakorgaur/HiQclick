#!/bin/bash

cd "$1" || return 0

docker-compose exec php-fpm ./vendor/bin/codecept run acceptance "$2" -vvv