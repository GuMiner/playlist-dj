import random
import sys

from config import genres
from player_state import PlayerState
from utility import math


class Playlist:
    def __init__(self, known_songs):
        self._known_songs = known_songs
        self._genre_list = list(self._known_songs)
        self._genre_song_list = None

    def _is_excluded_song(self, state, song):
        if not state.exclude_from_genre:
            return False

        song_genres = self._known_songs[state.genre][song]
        return any([genres.is_excluded_genre(genre) for genre in song_genres])

    def _next_song_index(self, state, advance):
        current_song_index = self._genre_song_list.index(state.song_path)

        next_song_index = current_song_index + advance
        next_song_index = math.clamp_and_wrap(next_song_index, len(self._genre_song_list))
        while self._is_excluded_song(state, self._genre_song_list[next_song_index]):
            next_song_index = next_song_index + advance
            next_song_index = math.clamp_and_wrap(next_song_index, len(self._genre_song_list))

        return next_song_index

    def _prep_song_list(self, genre, reset=False):
        if self._genre_song_list is None or reset:
            self._genre_song_list = list(self._known_songs[genre])
            random.shuffle(self._genre_song_list)

    def next_song(self, state):
        self._prep_song_list(state.genre)
        next_song_index = self._next_song_index(state, advance=1)
        return PlayerState(state.genre, self._genre_song_list[next_song_index], state.exclude_from_genre)

    def previous_song(self, state):
        self._prep_song_list(state.genre)
        next_song_index = self._next_song_index(state, advance=-1)
        return PlayerState(state.genre, self._genre_song_list[next_song_index], state.exclude_from_genre)

    def _is_excluded_genre(self, state, genre):
        if not state.exclude_from_genre:
            return False

        if genres.is_excluded_genre(genre):
            return True

        # A genre can still be excluded if it has no songs that also aren't excluded
        for song in self._known_songs[genre]:
            song_genres = self._known_songs[genre][song]
            if all([not genres.is_excluded_genre(genre) for genre in song_genres]):
                return False
        return True

    def _next_genre_index(self, state, advance):
        current_genre_index = self._genre_list.index(state.genre)
        next_genre_index = current_genre_index + advance
        next_genre_index = math.clamp_and_wrap(next_genre_index, len(self._genre_list))

        starting_index = next_genre_index
        while self._is_excluded_genre(state, self._genre_list[next_genre_index]):
            next_genre_index = next_genre_index + advance
            next_genre_index = math.clamp_and_wrap(next_genre_index, len(self._genre_list))

            if next_genre_index == starting_index:
                print("No songs exist which aren't excluded by genre")
                print("Reduce the exclusions in config.EXCLUDED_GENRES")
                sys.exit(-1)

        return next_genre_index

    def next_playlist(self, state):
        next_genre_index = self._next_genre_index(state, advance=1)

        next_genre = self._genre_list[next_genre_index]
        self._prep_song_list(next_genre, reset=True)

        print('Genre: {}'.format(next_genre))
        return PlayerState(next_genre, self._genre_song_list[len(self._genre_song_list) - 1], state.exclude_from_genre)

    def previous_playlist(self, state):
        next_genre_index = self._next_genre_index(state, advance=-1)

        next_genre = self._genre_list[next_genre_index]
        self._prep_song_list(next_genre, reset=True)

        print('Genre: {}'.format(next_genre))
        return PlayerState(next_genre, self._genre_song_list[len(self._genre_song_list) - 1], state.exclude_from_genre)

    def random_song_anywhere(self, state):
        genre = random.choice(self._genre_list)
        self._prep_song_list(genre, reset=True)

        song = random.choice(self._genre_song_list)

        print('Genre: {}'.format(genre))

        # state *can* be None, for first-time operation.
        exclude_from_genre = False if state is None else state.exclude_from_genre
        return PlayerState(genre, song, exclude_from_genre)

    def random_song_in_playlist(self, state):
        random_song = random.choice(self._genre_song_list)
        while self._is_excluded_song(state, random_song):
            random_song = random.choice(self._genre_song_list)

        return PlayerState(state.genre, random_song, state.exclude_from_genre)
