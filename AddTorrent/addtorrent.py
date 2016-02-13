#!/usr/bin/env  python3

#
# Copyright (c) 2016 Carlos Millett
#

import os
import sys
import notify2          # python-notify2
import subprocess
import configparser

config = os.environ.get("XDG_CONFIG_HOME")
if not config:
    config = os.path.expanduser("~/.config")

config = os.path.join(config, "addtorrent.conf")

opts = configparser.ConfigParser()
opts.read(config)

server = opts.get("default", "SERVER")
user = opts.get("default", "USER")
passw = opts.get("default", "PASSW")

magnet = sys.argv[-1]

cmd = ['transmission-remote', server, '-n', "{}:{}".format(user, passw), '-a', magnet]

notify2.init("Torrent")
summary = "Add"
text = "Connecting to server"
bubble = notify2.Notification(summary, text, "")
bubble.show()

try:
    subprocess.check_output(cmd, universal_newlines=True)
except subprocess.CalledProcessError as e:
    out = e.output
    summary, text = out.split(": ")
else:
    text = "Success!"

bubble.update(summary, text, "")
bubble.show()
