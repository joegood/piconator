__author__ = 'Joe'
import os
# adds the parent folder (of this) to the path
#os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load driver for your hardware, visualizer just for example
#from bibliopixel.drivers.visualizer import DriverVisualizer
from visualizer import DriverVisualizerWindow

#load the LEDMatrix class
from bibliopixel.led import *
from bibliopixel.animation import MatrixCalibrationTest

from PIL import Image, ImageSequence

from playlist import *
#import bibliopixel.image as image
import playlist_image_sequence_builder as imagebuilder

driver = DriverVisualizerWindow(width=32, height=32, stayTop=True, pixelSize=4)
try:

    #change rotation and vert_flip as needed by your display
    led = LEDMatrix(driver, rotation=MatrixRotation.ROTATE_0, vert_flip=False)

    #load calibration test animation
    #anim = MatrixCalibrationTest(led)

    playlist = load_playlist("playlist.json")

    try:

        anim = imagebuilder.PlaylistImageAnim(led, playlist)
        anim.run(untilComplete=True, max_cycles=1, sleep=150)

            #anim = image.ImageAnim(led, best_file)

            #anim.run(untilComplete=True, max_cycles=1, sleep=150)


    except KeyboardInterrupt:
        led.all_off()
        led.update()

finally:
    print "done..."
    '''
    # I spent WAY too much time trying to turn off the visualizer window.
    # 1) It it spawned in a seperate python process.
    # 2) I subclassed one of the Biblio Pixel driver files to return the process ID to me and tried to terminate direclty, which didn't work..  spawned threads.
    # 3) All of this because I was too lazy to click the [X] in the window... on a debugging process.. so I'm ending this exercise.
    # 4) If it becomes too annoying, I'll enumerate windows and kill via Win32 API.
    if driver.proc is not None:
        print "Terminating pid {}".format(driver.pid)
        driver.proc.terminate()
        driver.proc.kill()
        import signal
        ret = os.kill(driver.pid, signal.CTRL_C_EVENT)
        print ("CTRL_C_EVENT: ret = {0}".format(ret))
        ret = os.kill(driver.pid, signal.CTRL_BREAK_EVENT)
        print ("CTRL_BREAK_EVENT: ret = {0}".format(ret))
        ret = os.kill(driver.pid, 0)
        print ("0: ret = 0")
        ret = os.kill(driver.pid, signal.SIGTERM)
        print ("SIGTERM: ret = {}".format(ret))
    '''
