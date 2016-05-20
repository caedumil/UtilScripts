#!/usr/bin/env  bash

#
# Copyright (c) 2016 Carlos Millett
#

case ${1,,} in
    *black)
        index="color0"
        ;;&
    *red)
        index="color1"
        ;;&
    *green)
        index="color2"
        ;;&
    *yellow)
        index="color3"
        ;;&
    *blue)
        index="color4"
        ;;&
    *magenta)
        index="color5"
        ;;&
    *cyan)
        index="color6"
        ;;&
    *white)
        index="color7"
        ;;&
    bright* | bold*)
        index="color$(( ${index:5} + 8 ))"
        ;;
    color* | foreground | background)
        index="${1}"
        ;;
esac

echo $(xrdb -query | grep "${index}" | grep -E -m 1 -o "[A-Fa-f0-9]{6}")
