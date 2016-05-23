#!/usr/bin/env  bash

#Copyright (c) 2016 Carlos Millett
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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
