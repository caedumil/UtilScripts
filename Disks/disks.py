#!/usr/bin/env python3

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
        command = [ "devmon", self.action, self.mountpoint ]
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

safe = []
fail = []
prompt = "Media - unmount:" if args.umount else "Media - open:"
command = ["rofi", "-dmenu", "-p", prompt] if which("rofi") else \
    ["dmenu", "-p", prompt]

mountpts = [
        "/media/{0}".format(os.getenv("USER"))
    ,   "/media"
    ,   "/run/media/{0}".format(os.getenv("USER"))
]
for mpt in mountpts:
    if os.path.exists(mpt):
        mountpt = mpt
        break

with open("/etc/mtab") as arq:
    disks = [
        x.split(" ")[:2] for x in arq if
        ("/media/{0}".format(os.getenv("USER")) in x)
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
