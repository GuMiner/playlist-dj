import glob
import json
import os
import random

import config
from player_state import PlayerState
from progress import Progress
import song_analyzer


class Playlist:
    def __init__(self, known_songs):
        self.known_songs = known_songs
        self.genre_list = list(self.known_songs)
        self.genre_song_list = None

    @classmethod
    def load(cls):
        try:
            return cls._load_known_songs()
        except Exception as e:
            print('Could not load known songs list: {}'.format(str(e)))
            print('  Regenerating song db...')
            return cls._generate_song_db()

    @classmethod
    def _load_known_songs(cls):
        with open(config.KNOWN_SONGS_FILE, 'r') as json_file:
            known_songs = json.load(json_file)
            print('  Loaded known songs list with {} genres'.format(len(known_songs)))
            return cls(known_songs)

    def save_known_songs(self):
        try:
            with open(config.KNOWN_SONGS_FILE, 'w') as json_file:
                json.dump(self.known_songs, json_file)
        except Exception as e:
            print('  Failed to save known songs: {}'.format(str(e)))

    @staticmethod
    def _add_song_to_known(known_songs, genres, file):
        for genre in genres:
            if genre not in known_songs:
                known_songs[genre] = {}
            known_songs[genre][file] = genres

    @classmethod
    def _generate_song_db(cls):
        known_songs = {}
        song_count = 0
        progress = Progress(object='files', report_every=20)

        files = glob.glob(os.path.join(config.SONG_FOLDER, '**/*.*'))
        progress.start(count=len(files))

        files_with_genres = song_analyzer.scan_files(files, progress)
        for file_with_genre in files_with_genres:
            genres = file_with_genre['genres']
            file = file_with_genre['file']
            if genres is not None:
                song_count += 1
                Playlist._add_song_to_known(known_songs, genres, file)

        scan_time = progress.stop()
        print('    Found {} songs in {} genres in {:.2f} seconds.'.format(
            song_count, len(known_songs), scan_time))
        playlist = cls(known_songs)
        playlist.save_known_songs()
        return playlist

    @staticmethod
    def _clamp_to_range(index, size):
        if index >= size:
            index = 0
        elif index < 0:
            index = size - 1
        return index

    def _next_song_index(self, state, advance):
        current_song_index = self.genre_song_list.index(state.song_path)
        next_song_index = current_song_index + advance
        next_song_index = Playlist._clamp_to_range(next_song_index, len(self.genre_song_list))

        return next_song_index

    def _prep_song_list(self, genre, reset=False):
        if self.genre_song_list is None or reset:
            self.genre_song_list = list(self.known_songs[genre])

    def next_song(self, state):
        self._prep_song_list(state.genre)
        next_song_index = self._next_song_index(state, advance=1)
        return PlayerState(state.genre, self.genre_song_list[next_song_index])

    def previous_song(self, state):
        self._prep_song_list(state.genre)
        next_song_index = self._next_song_index(state, advance=-1)
        return PlayerState(state.genre, self.genre_song_list[next_song_index])

    def _next_genre_index(self, state, advance):
        current_genre_index = self.genre_list.index(state.genre)
        next_genre_index = current_genre_index + advance
        next_genre_index = Playlist._clamp_to_range(next_genre_index, len(self.genre_list))

        return next_genre_index

    def next_playlist(self, state):
        next_genre_index = self._next_genre_index(state, advance=1)

        next_genre = self.genre_list[next_genre_index]
        self._prep_song_list(next_genre, reset=True)

        print('Genre: {}'.format(next_genre))
        return PlayerState(next_genre, self.genre_song_list[len(self.genre_song_list) - 1])

    def previous_playlist(self, state):
        next_genre_index = self._next_genre_index(state, advance=-1)

        next_genre = self.genre_list[next_genre_index]
        self._prep_song_list(next_genre, reset=True)

        print('Genre: {}'.format(next_genre))
        return PlayerState(next_genre, self.genre_song_list[len(self.genre_song_list) - 1])

    def random_song_anywhere(self, state):
        genre = random.choice(self.genre_list)
        self._prep_song_list(genre, reset=True)

        song = random.choice(self.genre_song_list)
        return PlayerState(genre, song)

    def random_song_in_playlist(self, state):
        return PlayerState(state.genre, random.choice(self.genre_song_list))

    def toggle_excluded_genres(self):
        pass
