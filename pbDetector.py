import os
import shutil
import sys

"""
Usage: python pbDetector.py <input dir> <output dir>

Scans folder of ghost files sorted by track and copies out fastest
3lap and flap ghosts to separate folder
"""


scanFolder = sys.argv[1]

for track in os.listdir(scanFolder):
    trackPath = os.path.join(scanFolder, track)

    if track[0] == '.':
        continue

    fast3lap = 4294967295
    fast3lapFile = ""
    fastlap = 4294967295
    fastlapFile = ""

    for ghost in os.listdir(trackPath):    
        if ghost[0] == '.':
            continue

        ghostPath = os.path.join(trackPath, ghost)
        ghostFile = open(ghostPath, 'rb')
    
        # Find fastest 3-lap time #
        ghostFile.seek(0x1488, 0)
        curr3lap = int.from_bytes(ghostFile.read(4), "big")
        
        if curr3lap < fast3lap:
            fast3lap = curr3lap
            fast3lapFile = ghostPath

        # Find fastest flap time #
        ghostFile.seek(0x1490, 0)

        lapSum = 0

        for i in range(6):
            lapSplit = int.from_bytes(ghostFile.read(4), "big")
            
            if lapSplit == 0x5B8D7F:
                break

            currflap = lapSplit - lapSum
            if currflap < fastlap:
                fastlap = currflap
                fastlapFile = ghostPath

            lapSum = lapSplit

        currflap = curr3lap - lapSum # Final lap split not stored
        if currflap < fastlap:
            fastlap = currflap
            fastlapFile = ghostPath

    outputdir = sys.argv[2]

    coursefileObj = open(fast3lapFile, 'rb')
    coursefileObj.seek(0x146B, 0)
    courseTime = coursefileObj.read(8).decode().replace(":", "_")
    outputFile = track + "-" + courseTime + ".gci"
    shutil.copy(fast3lapFile,os.path.join(outputdir, outputFile))

    # Copy flap PB to output folder
    flapms = fastlap % 1000
    flapsecs = int(fastlap / 1000)
    flapmins = 0

    if flapsecs > 60:
        flapmins = int(flapsecs / 60)
        flapsecs = flapsecs - 60

    if flapmins != 0:
        outputFile = track + "-" +  str(flapmins) + "_" + f"{flapsecs:02}" + "_" + f"{flapms:03}" + ".gci"
    else:
        outputFile = track + "-" + f"{flapsecs:02}" + "_" + f"{flapms:03}" + ".gci"

    shutil.copy(fastlapFile, os.path.join(outputdir, outputFile))

