__author__ = 'Joe'
import os
# adds the parent folder (of this) to the path
#os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load driver for your hardware, visualizer just for example
from bibliopixel.drivers.visualizer import DriverVisualizer
driver = DriverVisualizer(width=32, height=32, stayTop=True)

#load the LEDMatrix class
from bibliopixel.led import *
#change rotation and vert_flip as needed by your display
led = LEDMatrix(driver, rotation=MatrixRotation.ROTATE_0, vert_flip=False)

from PIL import Image, ImageSequence
from playlist import *
#import bibliopixel.image as image
import playlist_image_sequence_builder as imagebuilder


#load calibration test animation
#from bibliopixel.animation import MatrixCalibrationTest
#anim = MatrixCalibrationTest(led)

playlist = load_playlist("playlist.json")


try:

    anim = imagebuilder.PlaylistImageAnim(led, playlist)

        #anim = image.ImageAnim(led, best_file)

        #anim.run(untilComplete=True, max_cycles=1, sleep=150)


except KeyboardInterrupt:
    led.all_off()
    led.update()
