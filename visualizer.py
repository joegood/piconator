__author__ = 'Joe'

'''
Copied/Forked from the Bibliopixel visualizer.py script.  I had to change it because I wanted to get the process ID
for the spawned visualizerUI.py process so I can close it programmatically.  I dislike having to click on the window
every time.  It appears that this may have been an idea in the beginning because the initial commit of this file on
GitHub has an import to subprocess.  It is an unused import in the existing code.  Let's use it...
'''

import os
import platform
import site
#import time
import subprocess
from bibliopixel.drivers.driver_base import *
from bibliopixel.drivers.network import *
import math

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bibliopixel.log as log


class DriverVisualizerWindow(DriverNetwork):
    """Main driver for Visualizer UI (for testing)"""

    def __init__(self, num=0, width=0, height=0, pixelSize=15, port=1618, stayTop=False):
        super(DriverVisualizerWindow, self).__init__(num, width, height, host="localhost", port=port)

        self.proc = None
        self.pid = 0

        allip = False

        if self.width == 0 and self.height == 0:
            self.width = self.numLEDs
            self.height = 1

        if self.numLEDs != self.width * self.height:
            raise ValueError("Provide either num OR width and height, but not all three.")

        try:
            #check if there is already a visualizer open and send dummy packet
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._host, self._port))
            s.send(bytearray([0,0,0]))
            s.close()
        except:
            operating_system = platform.system().lower()
            suffix = ""
            if "windows" in operating_system:
                exe_string = "start python"
            elif "darwin" in operating_system:
                exe_string = "python"
                suffix = "&"
            else:
                exe_string = "python"
                suffix = "&"

            '''
            originally, this class looked into its directory to find the visualizerUI.py file.
            since they now live in different directories, I need to look for the bibliopixel
            installation folder.  I'm going to assume a PIP install location.  Right now, PIP is all
            I am using.
            dname = os.path.dirname(os.path.abspath(__file__))
            script = '{}\\visualizerUI.py'.format(dname)
            '''

            script = ""
            for package_dir in site.getsitepackages():
                #print "package_dir = {0}".format(package_dir)
                script = os.path.join(package_dir, "bibliopixel\\drivers\\visualizerUI.py")
                #print "Searching for {}".format(script)
                #If we find the file in a path, break out of this loop
                if os.path.isfile(script):
                    break
                script = ""

            if len(script) == 0:
                print "Could not find the bibliopixel drivers visualizerUI.py script. Please make sure it is installed."
                raise IOError(2, "File {0} not found.".format(script))

            if allip:
                ip = "--allip"
            else:
                ip = ""

            if stayTop:
                top = "--top"
            else:
                top = ""

            arguments = "--width {0} --height {1} --pixelsize {2} --port {3} {4} {5} {6}"\
                .format(str(self.width),
                        str(self.height),
                        str(pixelSize),
                        str(port),
                        ip,
                        top,
                        suffix)

            command = "{0} \"{1}\" {2}".format(exe_string, script, arguments)
            print command
            log.logger.debug(command)

            import subprocess
            directive = ["python", script,
                         "--width", str(self.width),
                         "--height", str(self.height),
                         "--pixelsize", str(pixelSize),
                         "--port", str(port),
                         #ip,
                         top
                         ]
            print directive
            self.proc = subprocess.Popen(directive, shell=True)
            time.sleep(2)  # wait a little bit to let the proc spin up
            self.pid = self.proc.pid  # <--- access `pid` attribute to get the pid of the child process.

            #os.system(command)
            #time.sleep(2.0)

MANIFEST = [
    {
        "id": "visualizer",
        "class": DriverVisualizerWindow,
        "type": "driver",
        "display": "Visualizer",
        "params": [{
            "id": "num",
            "label": "# Pixels",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Total pixels in display. May use Width AND Height instead."
        }, {
            "id": "width",
            "label": "Width",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Width of display. Set if using a matrix."
        }, {
            "id": "height",
            "label": "Height",
            "type": "int",
            "default": 0,
            "min": 0,
            "help": "Height of display. Set if using a matrix."
        }, {
            "id": "pixelSize",
            "label": "Pixel Size",
            "type": "int",
            "default": 15,
            "min": 5,
            "max": 50,
            "help": "Size of rendered pixels in UI."
        }, {
            "id": "port",
            "label": "Port",
            "type": "int",
            "default": 1618,
            "help": "Port to connect to/listen on. Only change if using multiple visualizers.",
            "advanced": True
        }, {
            "id": "stayTop",
            "label": "Stay on Top",
            "type": "bool",
            "default": False,
            "help": "Force Visualizer UI to stay on top of all other windows.",
        }]
    }
]
