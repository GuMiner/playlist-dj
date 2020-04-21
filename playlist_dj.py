import readchar
import sys

import config
from playlist import Playlist
from player_state import PlayerState
from player import Player


def _print_help():
    # TODO add play/pause and don't use tabs!!!
    print('Commands:')
    print('  Operation:')
    print('    Toggle excluded genres:\t"{}"'.format(config.TOGGLE_EXCLUDED_GENRES_KEY))
    print('    Exit:\t\t\t\t\t"{}"'.format(config.QUIT_KEY))
    print('  Current Playlist:')
    print('    Next Song:\t\t"{}"'.format(config.NEXT_SONG_KEY))
    print('    Previous Song:\t"{}"'.format(config.PREVIOUS_SONG_KEY))
    print('    Random Song:\t"{}"'.format(config.RANDOM_SONG_IN_PLAYLIST_KEY))
    print('  Playlists:')
    print('    Next Playlist:\t\t\t"{}"'.format(config.NEXT_PLAYLIST_KEY))
    print('    Previous Playlist:\t\t"{}"'.format(config.PREVIOUS_PLAYLIST_KEY))
    print('    Random Song Anywhere:\t"{}"'.format(config.RANDOM_SONG_ANYWHERE_KEY))


def _play_and_save(current_player, player_state):
    current_player.play(player_state.song_path)
    player_state.save()


if __name__ == '__main__':
    print('Playlist DJ 1.0')
    _print_help()

    player = Player()
    song_list = Playlist.load()
    state = PlayerState.from_saved_state()

    if state is None:
        state = song_list.random_song_anywhere(state)
    _play_and_save(player, state)

    song_transition_map = {
        config.NEXT_SONG_KEY: song_list.next_song,
        config.PREVIOUS_SONG_KEY: song_list.previous_song,
        config.NEXT_PLAYLIST_KEY: song_list.next_playlist,
        config.PREVIOUS_PLAYLIST_KEY: song_list.previous_playlist,
        config.RANDOM_SONG_IN_PLAYLIST_KEY: song_list.random_song_in_playlist,
        config.RANDOM_SONG_ANYWHERE_KEY: song_list.random_song_anywhere
    }

    print('Waiting for command: ')
    while True:
        char = readchar.readchar().decode('utf-8').upper()
        if char in song_transition_map:
            state = song_transition_map[char](state)
            _play_and_save(player, state)
        elif char == config.PLAY_PAUSE_KEY:
            player.play_pause();
        elif char == config.TOGGLE_EXCLUDED_GENRES_KEY:
            song_list.toggle_excluded_genres()
        elif char == config.QUIT_KEY:
            player.stop_current_song()
            sys.exit(0)
        else:
            print('Unrecognized command "{}"'.format(char))
