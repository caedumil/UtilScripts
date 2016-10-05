#!/usr/bin/env  python3

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
import re
import sys
import configparser

import notify2
import transmissionrpc


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


transmission = transmissionrpc.Client(server, user=user, password=passw)


notify2.init("Torrent")
summary = "Add"
text = "Connecting to server"
bubble = notify2.Notification(summary, text, "")
bubble.show()


try:
    torrent = transmission.add_torrent(magnet)
    text = torrent.name

except transmissionrpc.error.TransmissionError as err:
    summary = "Error"
    text = re.findall('"(.*)"', err.message)[0]


bubble.update(summary, text, "")
bubble.show()
