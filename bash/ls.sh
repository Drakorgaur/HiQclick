#!/bin/bash

cd "$1" || return 0

# shellcheck disable=SC2010
ls | grep "$2"
