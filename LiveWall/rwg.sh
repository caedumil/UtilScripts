#!/usr/bin/env  bash

#
# Copyright (c) 2016 Carlos Millett
#

if [[ -z ${1} ]]; then
    (>&2 echo "Directory not specified")
    exit 1
fi

walldir="${1}"

find "${walldir}" -type f \( -iname "*.jpg" -o -iname "*.png" \) -print0 | \
    shuf --head-count=1 --zero-terminated | \
    xargs --null feh --bg-scale
