#!/usr/bin/env  bash

echo $(xrdb -query | grep ${1} | grep -E -m 1 -o "[A-Fa-f0-9]{6}")
