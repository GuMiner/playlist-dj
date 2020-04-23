import config
import glob
import json
import os

import song_analyzer
from utility import progress


def load():
    try:
        return _load_known_songs()
    except Exception as e:
        print('Could not load known songs list: {}'.format(str(e)))
        print('  Regenerating song db...')
        return _generate_song_db()


def _load_known_songs():
    with open(config.song_db.KNOWN_SONGS_FILE, 'r') as json_file:
        known_songs = json.load(json_file)
        print('  Loaded known songs list with {} genres'.format(len(known_songs)))
        return known_songs


def _add_song_to_known(known_songs, genres, file):
    for genre in genres:
        if genre not in known_songs:
            known_songs[genre] = {}
        known_songs[genre][file] = genres


def _generate_song_db():
    known_songs = {}
    song_count = 0
    progress_indicator = progress.Progress(scanning_object='files', report_every=20)

    files = glob.glob(os.path.join(config.environment.SONG_FOLDER, '**/*.*'))
    progress_indicator.start(count=len(files))

    files_with_genres = song_analyzer.scan_files(files, progress_indicator)
    for file_with_genre in files_with_genres:
        genres = file_with_genre['genres']
        file = file_with_genre['file']
        if genres is not None:
            song_count += 1
            _add_song_to_known(known_songs, genres, file)

    scan_time = progress_indicator.stop()
    print('    Found {} songs in {} genres in {:.2f} seconds.'.format(
        song_count, len(known_songs), scan_time))

    _save_known_songs(known_songs)
    return known_songs


def _save_known_songs(known_songs):
    try:
        with open(config.song_db.KNOWN_SONGS_FILE, 'w') as json_file:
            json.dump(known_songs, json_file)
    except Exception as e:
        print('  Failed to save known songs: {}'.format(str(e)))
