#!/usr/bin/env python3

# Copyright (c) 2020, Carlos Millett

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import subprocess as p


def run(cmd, **kwargs):
    ret = p.run(cmd, stdout=p.PIPE, **kwargs)
    return ret.stdout.decode('utf-8')


def screensaver_enabled():
    output = run(['xset', '-q'])
    return True if 'DPMS is Enabled' in output else False


def screensaver(is_enabled):
    if is_enabled:
        run(['xset', 's', 'off'])
        run(['xset', '-dpms'])
    else:
        run(['xset', 's', '600', '5'])
        run(['xset', 'dpms', '0', '0', '900'])


def bt_default_controller():
    controller = ''

    output = run(['bluetoothctl', 'list'])
    lines = output.splitlines()
    for ln in lines:
        if 'default' in ln:
            controller = ln.split()[1]
            break
    return controller

def bt_controller_enabled(controller):
    output = run(['bluetoothctl', 'show', controller])
    return False if 'Powered: no' in output else True


def bt_device_connected(device):
    output = run(['bluetoothctl', 'info', device])
    return False if 'Connected: no' in output else True


def bt_list_devices():
    output = run(['bluetoothctl', 'devices'])
    out_lines = output.splitlines()
    out_split = [x.split(maxsplit=2) for x in out_lines]
    return {k: v for _, v, k in out_split}


def menu(entries):
    cmd = ['rofi', '-dmenu', '-p', 'SESSION', '-width', '15', '-lines', '5']
    select = b'\n'.join([x.encode() for x in entries.keys()])
    output = run(cmd, input=select)

    key = output.strip()
    if not key:
        return

    func, args = entries[key]
    func(args)


def bluetooth(is_enabled):
    entries = {}

    if is_enabled:
        entries['Disable Bluetooth'] = (run, ['bluetoothctl', 'power', 'off'])

        devices = bt_list_devices()
        for dev in devices.keys():
            if bt_device_connected(devices[dev]):
                entries[f'Disconnect {dev}'] = (run, ['bluetooth' 'disconnect', devices[dev]])
            else:
                entries[f'Connect {dev}'] = (run, ['bluetoothctl', 'connect', devices[dev]])

    else:
        entries['Enable Bluetooth'] = (run, ['bluetoothctl', 'power', 'on'])

    menu(entries)


def main():
    entries = {}

    ss_is_on = screensaver_enabled()
    ss_status = 'ON' if ss_is_on else 'OFF'
    entries[f'ScreenSaver [{ss_status}]'] = (screensaver, ss_is_on)

    bt = bt_default_controller()
    bt_is_on = bt_controller_enabled(bt)
    bt_status = 'ON' if bt_is_on else 'OFF'
    entries[f'Bluetooth [{bt_status}]'] = (bluetooth, bt_is_on)

    entries.update({
        'Reload Session': (run, ['bspc', 'wm', '--restart']),
        'Reload HotKeys': (run, ['pkill', '-USR1', '-x', 'sxhkd']),
        'Reload GTK Theme': (run, ['pkill', '-HUP', '-x', 'xsettingsd'])
    })

    menu(entries)


if __name__ == '__main__':
    main()
