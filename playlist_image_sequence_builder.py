import datetime

__author__ = 'Joe'

import sys
import os
os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import glob

try:
    from PIL import Image, ImageSequence
except ImportError as e:
    error = "Please install Python Imaging Library: pip install pillow"
    raise ImportError(error)

from bibliopixel import colors
from bibliopixel.led import LEDMatrix
from bibliopixel.animation import BaseMatrixAnim

from playlist import *


# I originally wanted to subclass out the bibliopixel.image.ImageAnim class to add an initializer that could build from
# a playlist.  But, there is only one initializer on the original ImageAnim class, which required a file.  I don't want
# to use files, so I'm just forking and making something specific.


def findfile(filepath):
    """
    :param filepath: str
    """
    # these files are not being created large scale app, so there isn't any race conditions that can happen
    # where files are created after I check for their existence.

    # If the given path is correct, exit now, returning that path

    if os.path.isfile(filepath):
        return filepath

    locations = ["./", "./anim/", "./stills", "./img"]
    corename = os.path.basename(filepath)

    if __debug__:
        print "[{0}] was not found.  Trying [{2}] in locations: {1}".format(filepath, locations, corename)

    for loc in locations:
        filepath = os.path.join(loc, corename)
        if os.path.isfile(filepath):
            if __debug__:
                print "Found: {0}".format(filepath)
            return filepath

    raise IOError(2, "File {0} not found.".format(corename))


class PlaylistImageAnim(BaseMatrixAnim):  # inherit from bibliopixel.animation.BaseMatrixAnim

    def _getBufferFromImage(self, img, offset = (0,0)):
        duration = None
        if 'duration' in img.info:
            duration = img.info['duration']

        w = self._led.width - offset[0]
        if img.size[0] < w:
            w = img.size[0]

        h = self._led.height - offset[1]
        if img.size[1] < h:
            h = img.size[1]

        ox = offset[0]
        oy = offset[1]

        buffer = [0 for x in range(self._led.bufByteCount)]
        gamma = self._led.driver[0].gamma
        if self._bgcolor != (0,0,0):
            for i in range(self._led.numLEDs):
                buffer[i*3 + 0] = gamma[self._bgcolor[0]]
                buffer[i*3 + 1] = gamma[self._bgcolor[1]]
                buffer[i*3 + 2] = gamma[self._bgcolor[2]]

        frame = Image.new("RGBA", img.size)
        frame.paste(img)

        for x in range(ox, w + ox):
            for y in range(oy, h + oy):
                pixel = self._led.matrix_map[y][x]
                r, g, b, a = frame.getpixel((x - ox,y - oy))
                if a == 0:
                    r, g, b = self._bgcolor
                else:
                    r = (r * a) >> 8
                    g = (g * a) >> 8
                    b = (b * a) >> 8
                if self._bright != 255:
                    r, g, b = colors.color_scale((r, g, b), self._bright)

                buffer[pixel*3 + 0] = gamma[r]
                buffer[pixel*3 + 1] = gamma[g]
                buffer[pixel*3 + 2] = gamma[b]

        return buffer

    def _getBufferFromPath(self, imagePath, offset = (0,0)):
        img = Image.open(imagePath)
        return self._getBufferFromImage(img, offset)

    def __init__(self, led, plist, offset=(0, 0), bgcolor = colors.Off, brightness = 255):
        """

        :param offset:
        :param bgcolor:
        :param brightness:
        :param led: LEDMatrix
        :param plist: dict

        Helper class for building and displaying image animations for GIF files or a set of still bitmaps (png, gif,
        bmp, jpg) built from a playlist dictionary object.

        led - LEDMatrix instance
        plist - The dictionary loaded from the playlist.json file.
        offset - X,Y tuple coordinates at which to place the top-left corner of the image
        bgcolor - RGB tuple color to replace any transparent pixels with. Avoids transparent showing as black
        brightness - Brightness value (0-255) to scale the image by. Otherwise uses master brightness at the time of
                     instantiation.

        Key features of the playlist:
        1) It's JSON.  Example:
            {
              "1": {
                "file": "./anim/matrix.gif",
                "duration_s": 30,
                "frame_time_ms": 150
              },
              "2": {
                "file": "./anim/spinning balls.gif",
                "duration_s": 30,
                "frame_time_ms": 50
              },
              "3": {
                "file": "water.gif",
                "duration_s": 30
              }
            }
        2) Each item is indexed with something sortable.
        3) Each item contains the following attributes:
            file:  path to the file.  absolute path is tried first.  If not found, searches in ./anim and ./stills
            duration_s:  The duration in seconds that you wish to display the image or animation
            frame_time_ms:  The FPS, but in milliseconds

            Soon:
            fade_in:
            fade_out

        """
        super(PlaylistImageAnim, self).__init__(led)

        self._bright = brightness
        if self._bright == 255 and led.masterBrightness != 255:
            self._bright = led.masterBrightness

        self._bgcolor = colors.color_scale(bgcolor, self._bright)
        self._offset = offset
        self._images = []
        self._count = 0

        # check that our playlist has things...
        assert plist is not None, "Playlist is undefined"
        assert len(plist) > 0, "Playlist is empty"
        print("")
        print("Found {0} items in playlist...".format(len(plist)))

        self.drawCurrentTime()

        for key in sorted(plist):
            playlist_item = plist[key]
            print "%s: %s" % (key, playlist_item)

            img_file = ""
            duration_s = 30
            frame_time_ms = 150

            # find the image file.  if not found, skip.
            try:
                img_file = findfile(playlist_item[PLAYLIST_KEY_FILE])
            except IOError:
                print "{0} not found. Skipping.".format(img_file)
                continue  # skip to next item in dictionary

            # check the duration property.  if it's not there, default to 30
            try:
                if playlist_item[PLAYLIST_KEY_DURATION] > 0:
                    duration_s = playlist_item[PLAYLIST_KEY_DURATION]
            except KeyError:
                    duration_s = 30

            # check the frame rate.  if not there, default to 150ms per frame
            try:
                if playlist_item[PLAYLIST_KEY_FRAME_TIME] > 0:
                    frame_time_ms = playlist_item[PLAYLIST_KEY_FRAME_TIME]
            except KeyError:
                frame_time_ms = 150

            # load the image
            img = Image.open(img_file)

            # debug print some image properties
            print "\t>>>>>>>>>> {}".format(img.filename)
            print "\tformat: {}".format(img.format)
            print "\tmode: {}".format(img.mode)
            print "\tsize: {}".format(img.size)
            print "\twidth: {}".format(img.width)
            print "\theight: {}".format(img.height)
            print "\tinfo: {}".format(img.info)
            if getattr(img, "is_animated", False):
                print "\tis_animated: {}".format(img.is_animated)
                print "\tn_frames: {}".format(img.n_frames)
            else:
                print "\tis_animated: False"
                print "\tn_frames: 0"
            print ""

            # assign everything back into the dictionary and we will make an array of those to produce the frames
            playlist_item[PLAYLIST_KEY_FILE] = img_file
            playlist_item[PLAYLIST_KEY_DURATION] = duration_s
            playlist_item[PLAYLIST_KEY_FRAME_TIME] = frame_time_ms

            # if this is a .gif, we need to pull an image for each frame and assign that a slot in the animation.
            # if it is another raster, just load it

            # TODO: Determine if animatd gifs can be resized in PIL and all frames are processed
            # TODO: Determine if there is some universal format that the images need to be translated into

            if img_file.endswith(".gif"):
                for frame in ImageSequence.Iterator(img):
                    # copy the frame info from the playlist so we can just add a new binary
                    gif_playlist_item = playlist_item.copy()
                    gif_playlist_item[PLAYLIST_KEY_BINARYIMAGE] = self._getBufferFromImage(frame)
                    self._images.append(gif_playlist_item)
                    self._count += 1
            else:
                playlist_item[PLAYLIST_KEY_BINARYIMAGE] = self._getBufferFromImage(img)
                self._images.append(playlist_item)
                self._count += 1




        '''
        # this code centers smaller images into the LED frame then adds them into the animation array, that is
        # later used by the .step method to update the frame in the LED.
        # In the playlist version, I want to resize all images to fit the matrix, so centering will not be needed.
        # Adding to the array will be needed.

        if imagePath.endswith(".gif"):
            log.logger.info("Loading {0} ...".format(imagePath))
            img = Image.open(imagePath)
            if self._offset == (0,0):
                w = 0
                h = 0
                if img.size[0] < self._led.width:
                    w = (self._led.width - img.size[0]) / 2
                if img.size[1] < self._led.height:
                    h = (self._led.height - img.size[1]) / 2
                self._offset = (w, h)

            for frame in ImageSequence.Iterator(img):
                self._images.append(self._getBufferFromImage(frame, self._offset))
                self._count += 1
        else:
            imageList = glob.glob(imagePath + "/*.bmp")
            imageList.sort()

            self._count = len(imageList)
            if self._count == 0:
                raise ValueError("No images found!")

            for img in imageList:
                if self._offset == (0,0):
                    if img.size[0] < self._led.width:
                        self._offset[0] = (self._led.width - img.size[0]) / 2
                    if img.size[1] < self._led.height:
                        self._offset[1] = (self._led.height - img.size[1]) / 2

                self._images.append(self._getBufferFromPath(img, self._offset))
        '''

        self._curImage = 0

    def drawCurrentTime(self):
        """
        :rtype : None
        """
        self._led.all_off()
        # at size=1, chars are 6 pixels wide, 8 tall.  1 pad pixel on bottom and right of block
        from datetime import datetime
        d = datetime.now()
        self._led.drawText("{:%I:%M}".format(d), 1, 1, colors.White, colors.Off, 1)
        self._led.drawText("{:%b%d}".format(d), 1, 10, colors.Gray, colors.Off, 1)
        self._led.drawText("{:%Y}".format(d), 1, 19, colors.Gray, colors.Off, 1)
        self._led.update()

    def preRun(self):
        self._curImage = 0

    # this is called by the base class to actually do the drawing of the frame
    def step(self, amt=1):
        self._led.all_off()

        # instead of having a {duration, buffer} tupple in the _images array, it is a dictionary with:
        # PLAYLIST_KEY_FILE = "file"
        # PLAYLIST_KEY_DURATION = "duration_s"
        # PLAYLIST_KEY_FRAME_TIME = "frame_time_ms"
        # PLAYLIST_KEY_BINARYIMAGE = "binaryimage"

        buffer = self._images[self._curImage][PLAYLIST_KEY_BINARYIMAGE]
        frameTime = self._images[self._curImage][PLAYLIST_KEY_FRAME_TIME]

        self._led.setBuffer(buffer)
        self._internalDelay =frameTime

        self._curImage += 1
        if self._curImage >= self._count:
            self._curImage = 0
            self.animComplete = True

        self._step = 0

