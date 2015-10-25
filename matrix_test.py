__author__ = 'Joe'
import os
# adds the parent folder (of this) to the path
#os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load driver for your hardware, visualizer just for example
from bibliopixel.drivers.visualizer import DriverVisualizer

from PIL import Image, ImageSequence

from playlist import *

driver = DriverVisualizer(width=32, height=32, stayTop=True)

#load the LEDMatrix class
from bibliopixel.led import *
#change rotation and vert_flip as needed by your display
led = LEDMatrix(driver, rotation=MatrixRotation.ROTATE_0, vert_flip=False)

#load calibration test animation
#from bibliopixel.animation import MatrixCalibrationTest
#anim = MatrixCalibrationTest(led)

playlist = load_playlist("playlist.json")

animPath = "./anim/"
stillsPath = "./stills/"

import bibliopixel.image as image

try:

    for key in sorted(playlist):
        playlist_item = playlist[key]
        print "%s: %s" % (key, playlist_item)

        # Meh, I hate the way this looks..
        # REFACTOR: turn this into a function.
        best_file = playlist_item["file"]  # this is the provided path

        found = os.path.isfile(best_file)

        # If the file is not found, trim the path info and try in our known folders
        if not found:
            core_file = os.path.basename(best_file)
            print "[%s] was not found.  Trying [%s] in known folders..." % (best_file, core_file)
            best_file = os.path.join(animPath, core_file)
            found = os.path.isfile(best_file)

            if not found:
                best_file = os.path.join(stillsPath, core_file)
                found = os.path.isfile(best_file)

        if found:
            print "Found [%s]" % best_file

        else:
            print "[%s] was not found." % best_file
            continue  # for

        anim = image.ImageAnim(led, best_file)
        anim.run(untilComplete=True, max_cycles=1, sleep=150)


except KeyboardInterrupt:
    led.all_off()
    led.update()
