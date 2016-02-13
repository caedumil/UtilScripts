# Disks

Script to list mounted removable USB drives.

Use `dmenu`, or `rofi` if avaliable, to show all mounted flash drives. Selected
entry opens a terminal window on mounted path.

## Requires

* python 3
* rofi or dmenu
* ranger

## Usage

    disks [-u]

Open selected entry by default.
Using `-u` the selected entry is unmounted.
