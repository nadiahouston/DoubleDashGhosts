import time
import os
import sys

"""
Usage: python rename.py <input dir> <output dir>

Looks at folder of ghost files and both sorts them by course and renames them
with the track and time.
"""

input_directory  = sys.argv[1]
output_directory = sys.argv[2]

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

for file in os.listdir(input_directory):
    if file[0] == ".":
        continue

    ghost = os.path.join(input_directory, file)

    f = open(ghost, 'rb')
    f.seek(0x28, 0)
    timestamp = int.from_bytes(f.read(4), "big") # Time in s since Jan 1 2000
    timestamp = timestamp + 946684800 # Time in s since Jan 1 1970
    date = time.strftime('%Y-%m-%d', time.gmtime(timestamp))

    f.seek(0x1483, 0)
    track = int.from_bytes(f.read(1), "big")

    track_names = {0x24:"LC", 0x22:"PB",  0x21:"BP", 0x32:"DDD",
                   0x28:"MB", 0x25:"MaC", 0x23:"DC", 0x2A:"WS",
                   0x33:"SL", 0x29:"MuC", 0x26:"YC", 0x2D:"DKM",
                   0x2B:"WC", 0x2C:"DDJ", 0x2F:"BC", 0x31:"RR"}

    f.seek(0x146B, 0)
    track_name = track_names[track] if track in track_names else "null"
    courseTime = f.read(8).decode().replace(":", "_")

    if not os.path.exists(os.path.join(output_directory, track_name)):
        os.mkdir(os.path.join(output_directory, track_name))

    new_filename = track_name + "-" + date  + "-" + courseTime + ".gci"
    new_filepath = os.path.join(output_directory, track_name, new_filename) 

    if os.path.isfile(new_filepath):
        os.remove(ghost)
    else:
        os.rename(ghost, new_filepath)
