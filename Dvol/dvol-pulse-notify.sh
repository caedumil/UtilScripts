#!/bin/bash

#
# Original code by: bruening ( https://bbs.archlinux.org/viewtopic.php?id=46608 )
# Modified by: caedus75
#

#Probably do not customize
PIPE="/tmp/dvolpipe"

err() {
    echo "${1}"
    exit 1
}

usage() {
    echo "usage: dvol [option] [argument]"
    echo
    echo "Options:"
    echo "     -i, --increase - increase volume by 'argument'"
    echo "     -d, --decrease - decrease volume by 'argument'"
    echo "     -t, --toggle   - toggle mute on and off"
    echo "     -h, --help     - display this"
    exit
}

#Argument Parsing
case "${1}" in
    '-i'|'--increase')
        [ -z "${2}" ] && err "No argument specified for increase."
        ARG="increase ${2}"
        ;;
    '-d'|'--decrease')
        [ -z "${2}" ] && err "No argument specified for decrease."
        ARG="decrease ${2}"
        ;;
    '-t'|'--toggle')
        ARG="toggle"
        ;;
    ''|'-h'|'--help')
        usage
        ;;
    *)
        err "Unrecognized option '${1}', see dvol --help"
        ;;
esac

#Actual volume changing
VOL="$(ponymix ${ARG})"
ponymix is-muted && VOL="0"

#Using named pipe to determine whether previous call still exists
#Also prevents multiple volume bar instances
if [ ! -e "${PIPE}" ]; then
    mkfifo "${PIPE}"
    ( notify-send\
        -t 25\
        -a "Volume"\
        "$(cat "${PIPE}")"
    rm -f "${PIPE}" ) &
fi

#Feed the pipe!
( echo "${VOL}" | dbar ) > "${PIPE}"
