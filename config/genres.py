# Any file that includes any of these genres won't be played by default,
#  unless the TOGGLE_EXCLUDED_GENRES key is pressed.
EXCLUDED_GENRES = ['Explicit', 'MIDI', 'Humor']


def is_excluded_genre(genre):
    return any([genre.upper() == excluded_genre.upper() for excluded_genre in EXCLUDED_GENRES])
