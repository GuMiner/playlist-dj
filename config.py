# Keys 'ir-keytable' outputs to control the playlist DJ
PLAY_PAUSE_KEY = ' '
NEXT_SONG_KEY = 'A'
PREVIOUS_SONG_KEY = 'B'

NEXT_PLAYLIST_KEY = 'C'
PREVIOUS_PLAYLIST_KEY = 'D'

RANDOM_SONG_IN_PLAYLIST_KEY = 'E'
RANDOM_SONG_ANYWHERE_KEY = 'F'

TOGGLE_EXCLUDED_GENRES_KEY = 'G'

QUIT_KEY = 'Q'

# Any file that includes any of these genres won't be played by default,
#  unless the TOGGLE_EXCLUDED_GENRES key is pressed.
EXCLUDED_GENRES = ('Explicit',)

LAST_PLAYER_STATE_FILE = 'last-player-state.json'
KNOWN_SONGS_FILE = 'known-songs.json'

SONG_FOLDER = r'ABSOLUTE_PATH'

EXIF_TOOL_PATH = r'...\exiftool.exe'
FFPLAY_TOOL_PATH = r'...\ffplay.exe'
