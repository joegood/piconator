__author__ = 'Joe'

import json


PLAYLIST_KEY_FILE = "file"
PLAYLIST_KEY_DURATION = "duration_s"
PLAYLIST_KEY_FRAME_TIME = "frame_time_ms"


#just a simple function call now until I build out a proper object
def load_playlist(playlist_name='playlist.json'):

    json_file = open(playlist_name)
    playlist = json.load(json_file)

    print "Loaded playlist (" + playlist_name + ")..."

    json_file.close()

    print "type(playlist) = {}".format(type(playlist))

    return playlist
