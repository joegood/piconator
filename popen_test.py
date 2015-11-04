__author__ = 'Joe'

import sys
print "sys.argv---"
print sys.argv
print "-----------"
print ""

import argparse
parser = argparse.ArgumentParser(description='Test Parser')
parser.add_argument('--width', help='Matrix Width', required=True, type=int)
parser.add_argument('--height', help='Matrix Height', default=1, type=int)
parser.add_argument('--pixelsize', help='width/height of pixels in visualizer (default: 10)', default=10, type=int)
parser.add_argument('--top', help='Keep the visualizer on top of all other windows', action='store_true')
parser.add_argument('--port', help='Advanced: TCP port to listen on (default: 1618)', default=1618, type=int)
parser.add_argument('--allip', help='Visualizer will listen for data on all network connections', action='store_true')

args = vars(parser.parse_args())

width = args['width']
height = args['height']
pixelSize = args['pixelsize']
top = args['top']
port = args['port']
allip = args['allip']
