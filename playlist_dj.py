import readchar
import sys

import config
from playlist import Playlist
from player_state import PlayerState
from player import Player


def _print_help():
    print('Commands:')
    print('  Operation:')
    print('    Play/Pause:              "{}"'.format(config.PLAY_PAUSE_KEY))
    print('    Toggle excluded genres:  "{}"'.format(config.TOGGLE_EXCLUDED_GENRES_KEY))
    print('    Exit:                    "{}"'.format(config.QUIT_KEY))
    print('  Current Playlist:')
    print('    Next Song:               "{}"'.format(config.NEXT_SONG_KEY))
    print('    Previous Song:           "{}"'.format(config.PREVIOUS_SONG_KEY))
    print('    Random Song:             "{}"'.format(config.RANDOM_SONG_IN_PLAYLIST_KEY))
    print('  Playlists:')
    print('    Next Playlist:           "{}"'.format(config.NEXT_PLAYLIST_KEY))
    print('    Previous Playlist:       "{}"'.format(config.PREVIOUS_PLAYLIST_KEY))
    print('    Random Song Anywhere:    "{}"'.format(config.RANDOM_SONG_ANYWHERE_KEY))


def _play_and_save(current_player, player_state):
    current_player.play(player_state.song_path)
    player_state.save()


if __name__ == '__main__':
    print('Playlist DJ 1.0')
    _print_help()

    song_list = Playlist.load()
    state = PlayerState.from_saved_state()

    if state is None:
        state = song_list.random_song_anywhere(state)

    print('Genre: {}'.format(state.genre))

    def _next_song():
        global state
        state = song_list.next_song(state)
        _play_and_save(player, state)

    player = Player(next_song_callback=_next_song)
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
    alive = True
    while alive:
        char = readchar.readchar().decode('utf-8').upper()

        # Don't move to the next song automatically when processing a command
        with player.song_action_mutex:
            if char in song_transition_map:
                state = song_transition_map[char](state)
                _play_and_save(player, state)
            elif char == config.PLAY_PAUSE_KEY:
                player.play_pause()
            elif char == config.TOGGLE_EXCLUDED_GENRES_KEY:
                song_list.toggle_excluded_genres()
            elif char == config.QUIT_KEY:
                alive = False
            else:
                print('Unrecognized command "{}"'.format(char))

    player.terminate()
    sys.exit(0)