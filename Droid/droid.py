#!/usr/bin/env  python3

#
# Copyright (c) 2016 Carlos Millett
#

import os
import re
import sys
import argparse
import subprocess as proc

#
# Main
#
ex = os.EX_OK

list_cmd = ["simple-mtpfs", "--list-devices"]
mount_cmd = ["simple-mtpfs", "--device"]
umount_cmd = ["fusermount", "-u"]

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-m", "--mount", action="store_true",
    help="mount devices")
group.add_argument("-u", "--umount", action="store_true",
    help="unmount devices")

args = parser.parse_args()

if not (args.mount or args.umount):
    parser.print_help()
    sys.exit(ex)

try:
    regex = re.compile("(\d): (\w{5,8})")

    pref = os.path.expanduser("~")

    out = proc.check_output(list_cmd, stderr=proc.STDOUT)
    dev_list = out.decode("utf-8").splitlines()

    dev_dict = {
        x.group(1): os.path.join(pref, x.group(2)) for x in
        [ regex.search(y) for y in dev_list ] }

    if args.mount:
        for key, value in dev_dict.items():
            path = os.path.join(pref, value)

            if os.path.ismount(path):
                continue

            os.makedirs(path, 0o755)
            proc.check_output(mount_cmd+[key, path], stderr=proc.STDOUT)

            print("Success! Device {0} mounted as {1}".format(key, path))

    elif args.umount:
        for value in dev_dict.values():
            path = os.path.join(pref, value)

            if not os.path.ismount(path):
                continue

            proc.check_output(umount_cmd+[path], stderr=proc.STDOUT)
            os.rmdir(path)

            print("Success! Unmounted {}".format(path))

except OSError as err:
    print(err.strerror)
    ex = err.errno

except proc.CalledProcessError as err:
    print(err.output.decode("utf-8"))
    ex = err.returncode

finally:
    sys.exit(ex)
