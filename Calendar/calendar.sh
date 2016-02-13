#!/bin/bash

#
# Copyright (c) 2007, by Robert Manea
# http://dzen.geekmode.org/dwiki/doku.php?id=dzen:calendar
# modified by urukrama
# modified by caedus75
#

FG="#$(getXresColor foreground)"
BG="#$(getXresColor background)"
X="1080"
Y="16"
W="200"

TODAY=$(expr $(date +'%d') + 0)
MONTH=$(date +'%m')
YEAR=$(date +'%Y')

(
echo `date +'%a %d %B %Y %n'`
echo

# current month, hilight header and today
cal | sed -re "s/(^|[ ])(${TODAY})($|[ ])/\1^bg(${FG})^fg(${BG})\2^fg()^bg()\3/"

sleep 8
)\
    | dzen2\
        -x ${X}\
        -y ${Y}\
        -w ${W}\
        -l 9\
        -sa c\
        -e 'button3=exit;onstart=uncollapse;'-
