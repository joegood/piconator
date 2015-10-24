__author__ = 'Joe'

import json


#just a simple function call now until I build out a proper object
def load_playlist(playlist_name='playlist.json'):

    json_file = open(playlist_name)
    playlist = json.load(json_file)

    print "Loaded playlist (" + playlist_name + ")..."

    json_file.close()

    return playlist
