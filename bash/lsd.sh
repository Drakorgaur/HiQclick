#!/bin/bash

cd "$1" || return 0

# shellcheck disable=SC2010
# shellcheck disable=SC2035
ls -d */
