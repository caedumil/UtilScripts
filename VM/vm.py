#!/usr/bin/env python3

#
# Copyright (c) 2016 Carlos Millett
#

import os
import sys
import notify2
import argparse
import configparser
import subprocess as p

#
# Functions
#
def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("-e", "--entry", default="default",
        type=str, help="entry on config file")

    return parser.parse_args()

def config_path():
    vmconf = os.environ.get("XDG_CONFIG_HOME")
    if vmconf == None:
        vmconf = os.path.expanduser("~/.config")

    return os.path.join(vmconf, "vm.conf")

def conf(path, entry):
    opt = {}

    config = configparser.ConfigParser()

    config.read(path)

    opt["user"] = config[entry].get("USER", "")
    opt["passw"] = config[entry].get("PASSW", "")
    opt["ip"] = config[entry].get("IP", "")

    return opt

#
# Main
#
args = cli()

opts = conf(config_path(), args.entry)

notify2.init("RemoteDesk")
bubble = notify2.Notification("", "", "")

command = "xfreerdp"

try:
    print("Connecting to {}".format(opts["ip"]))
    bubble.update("", "Connecting to host", "")
    bubble.show()

    with open(os.devnull, "wb") as quiet:
        p.check_call([command,
            "+kbd:0x10416", "+size:1024x768", "+network:lan", "+compression",
            "+u:"+opts["user"], "+p:"+opts["passw"], "+v:"+opts["ip"]],
            stdout=quiet)
        end = "Connection closed"

except p.CalledProcessError:
    end = "Connection failed"

except KeyError:
    end = "Invalid entry"

finally:
    print(end)
    bubble.update("", end, "")
    bubble.show()

# Say goodbye and exit
sys.exit(os.EX_OK)
