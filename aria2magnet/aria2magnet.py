#!/usr/bin/env python3

# ================================================================

# Python3 port of:
# https://github.com/smasterfree/aria-control-file-parser

# ================================================================


# ================================================================
#  0                   1                   2                   3
#  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
# +---+-------+-------+-------------------------------------------+
# |VER|  EXT  |INFO   |INFO HASH ...                              |
# |(2)|  (4)  |HASH   | (INFO HASH LENGTH)                        |
# |   |       |LENGTH |                                           |
# |   |       |  (4)  |                                           |
# +---+---+---+-------+---+---------------+-------+---------------+
# |PIECE  |TOTAL LENGTH   |UPLOAD LENGTH  |BIT-   |BITFIELD ...   |
# |LENGTH |     (8)       |     (8)       |FIELD  | (BITFIELD     |
# |  (4)  |               |               |LENGTH |  LENGTH)      |
# |       |               |               |  (4)  |               |
# +-------+-------+-------+-------+-------+-------+---------------+
# |NUM    |INDEX  |LENGTH |PIECE  |PIECE BITFIELD ...             |
# |IN-    |  (4)  |  (4)  |BIT-   | (PIECE BITFIELD LENGTH)       |
# |FLIGHT |       |       |FIELD  |                               |
# |PIECE  |       |       |LENGTH |                               |
# |  (4)  |       |       |  (4)  |                               |
# +-------+-------+-------+-------+-------------------------------+
#
#         ^                                                       ^
#         |                                                       |
#         +-------------------------------------------------------+
#                 Repeated in (NUM IN-FLIGHT) PIECE times

# more detail
# https://aria2.github.io/manual/en/html/technical-notes.html
# ================================================================


import sys
import argparse


def parse_aria_control_file():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'file',
        nargs='+',
        help='input file XXX.aria2'
    )
    args = parser.parse_args()
    file_list = args.file

    for file_name in file_list:
        with open(file_name, "rb") as f:
            # Go to beginning, read VER
            f.seek(0)
            version = f.read(2)
            ver = int.from_bytes(version, byteorder='big')

            # skip  EXT, find info hash_binary length
            f.seek(6)
            length = f.read(4)
            hash_length = int.from_bytes(length, byteorder='big')

            # For http/ftp downloads, this value should be 0
            if hash_length == 0:
                print("Not a torrent.", file=sys.stderr)
                continue

            # Read next info hash
            f.seek(10)
            hash_binary = f.read(hash_length)
            info_hash = bytes.hex(hash_binary)

        magnet_link = "magnet:?xt=urn:btih:{}".format(info_hash)
        print(magnet_link)


if __name__ == '__main__':
    parse_aria_control_file()
