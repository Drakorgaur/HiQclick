#!/bin/bash

cd "$1" || return 0

# shellcheck disable=SC2002
cat "$2" | grep "$3"
