#!/usr/bin/env python3

#
# Copyright (c) 2015-2016 Carlos Millett
#

import os
import sys
import notify2
import argparse
import subprocess as p

from shutil import which

#
# Class
#
class Media():
    def __init__(self, devpath, mountpoint):
        self.devpath = devpath
        self.mountpoint = mountpoint
        self.label = os.path.basename(mountpoint)
        self.action = "--eject" if "/sr" in devpath else "--unmount"

    def __str__(self):
        return "{}\t( {} )".format(self.label, self.devpath)

    def explore(self):
        command = [
            "urxvt", "-name", "Ranger", "-cd", self.mountpoint, "-e", "ranger"
        ]
        p.call(command)
        return

    def umount(self):
        command = [ "devmon", self.action, self.devpath ]
        try:
            p.check_call(command)
            return True

        except p.CalledProcessError:
            return False

#
# Main
#
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--umount", action="store_true",
    help="unmount devices")
args = parser.parse_args()

notify2.init("Media")

safe = []
fail = []
prompt = "Media - unmount:" if args.umount else "Media - open:"
command = ["rofi", "-dmenu", "-p", prompt] if which("rofi") else \
    ["dmenu", "-p", prompt]

with open("/etc/mtab") as arq:
    disks = [
        x.split(" ")[:2] for x in arq if
        ("/dev/sd" in x and "/sda" not in x) or "/sr" in x
    ]

devs = {
    str(x):x for x in [ Media(x, y.replace("\\040", " ")) for x, y in disks ]
}
labels = b"\n".join([ bytes(x, "UTF-8") for x in devs.keys() ])

menu = p.Popen(command, stdout=p.PIPE, stdin=p.PIPE)
pick = [ x.decode() for x in menu.communicate(input=labels)[0].splitlines() ]

if len(pick) > 0 and args.umount:
    for x in pick:
        status = devs[x].umount()

        if status:
            safe.append(devs[x].label)
        else:
            fail.append(devs[x].label)

    if safe:
        message = " - ".join(safe)
        safe_pop = notify2.Notification("Safe to remove", message, "")
        safe_pop.show()

    if fail:
        message = " - ".join(fail)
        fail_pop = notify2.Notification("Failed", message, "")
        fail_pop.set_urgency(notify2.URGENCY_CRITICAL)
        fail_pop.show()

elif len(pick) == 1:
    devs[pick[0]].explore()

sys.exit(0)
