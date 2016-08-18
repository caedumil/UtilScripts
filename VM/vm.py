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
import configparser
import subprocess as p

#
# Main
#
parser = argparse.ArgumentParser()
parser.add_argument(
    "-e", "--entry", default="default", type=str,
    help="entry on config file"
)
parser.add_argument(
    "-n", "--notify", action="store_true",
    help="use notification bubbles to display messages"
)
args = parser.parse_args()


vmconf = os.environ.get("XDG_CONFIG_HOME")
if vmconf == None:
    vmconf = os.path.expanduser("~/.config")


opt = {}
config = configparser.ConfigParser()
config.read(os.path.join(vmconf, "vm.conf"))

opt["user"] = config[args.entry].get("USER", "")
opt["passw"] = config[args.entry].get("PASSW", "")
opt["ip"] = config[args.entry].get("IP", "")


if args.notify:
    notify2.init("RemoteDesk")
    bubble = notify2.Notification("", "", "")


command = "xfreerdp"
try:
    print("Connecting to {}".format(opt["ip"]))
    if args.notify:
        bubble.update("", "Connecting to host", "")
        bubble.show()

    p.check_call([command,
        "+kbd:0x10416", "+size:1024x768", "+network:lan", "+compression",
        "+u:"+opt["user"], "+p:"+opt["passw"], "+v:"+opt["ip"]],
        stdout=p.DEVNULL, stderr=p.DEVNULL)
    end = "Connection closed"

except p.CalledProcessError:
    end = "Connection failed"

except KeyError:
    end = "Invalid entry"

finally:
    print(end)
    if args.notify:
        bubble.update("", end, "")
        bubble.show()

# Say goodbye and exit
sys.exit(os.EX_OK)
