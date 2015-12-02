__author__ = 'Joe'

import json


PLAYLIST_KEY_FILE = "file"
PLAYLIST_KEY_DURATION = "duration_s"
PLAYLIST_KEY_FRAME_TIME = "frame_time_ms"
PLAYLIST_KEY_BINARYIMAGE = "binaryimage"
PLAYLIST_KEY_LOOP_ROOT = "looproot"


#just a simple function call now until I build out a proper object
def load_playlist(playlist_name='playlist.json'):

    json_file = open(playlist_name)
    playlist = json.load(json_file)
    json_file.close()

    print ""
    print "Loaded playlist (" + playlist_name + ")..."
    print repr(playlist)
    print "type(playlist) = {}".format(type(playlist))

    return playlist


# define an object to deserialize our json into
class PlaylistItem(object):
    def __init__(self, file, duration_s, frame_time_ms):
        self.imagefile = file
        self.duration_s = duration_s
        self.frame_time_ms = frame_time_ms
