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
