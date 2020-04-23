import readchar
import sys

from config import keys, environment
import known_songs_state
from playlist import Playlist
from player_state import PlayerState
from player import Player


def _print_help():
    print('Commands:')
    print('  Operation:')
    print('    Play/Pause:              "{}"'.format(keys.PLAY_PAUSE_KEY))
    print('    Toggle excluded genres:  "{}"'.format(keys.TOGGLE_EXCLUDED_GENRES_KEY))
    print('    Exit:                    "{}"'.format(keys.QUIT_KEY))
    print('  Current Playlist:')
    print('    Next Song:               "{}"'.format(keys.NEXT_SONG_KEY))
    print('    Previous Song:           "{}"'.format(keys.PREVIOUS_SONG_KEY))
    print('    Random Song:             "{}"'.format(keys.RANDOM_SONG_IN_PLAYLIST_KEY))
    print('  Playlists:')
    print('    Next Playlist:           "{}"'.format(keys.NEXT_PLAYLIST_KEY))
    print('    Previous Playlist:       "{}"'.format(keys.PREVIOUS_PLAYLIST_KEY))
    print('    Random Song Anywhere:    "{}"'.format(keys.RANDOM_SONG_ANYWHERE_KEY))


def _play_and_save(current_player, player_state):
    current_player.play(player_state.song_path)
    player_state.save()


def _resume_playing_on_start(current_player, player_state):
    print('Genre: {}'.format(player_state.genre))
    _play_and_save(current_player, state)


def _end_program():
    if shutdown and environment.is_linux():
        import subprocess
        result = subprocess.run(["gnome-session-quit", "--power-off", "--force"],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        print("shutdown: {}: {}", result.returncode, result.stdout)
    elif shutdown:
        print('Shutdown is not implemented on Windows yet, sorry.')

    sys.exit(0)


if __name__ == '__main__':
    print('Playlist DJ 2.0')
    _print_help()

    song_list = Playlist(known_songs_state.load())
    state = PlayerState.from_saved_state()

    if state is None:
        state = song_list.random_song_anywhere(state)

    def _next_song():
        global state
        state = song_list.next_song(state)
        _play_and_save(player, state)

    player = Player(next_song_callback=_next_song)
    _resume_playing_on_start(player, state)

    song_transition_map = {
        keys.NEXT_SONG_KEY: song_list.next_song,
        keys.PREVIOUS_SONG_KEY: song_list.previous_song,
        keys.NEXT_PLAYLIST_KEY: song_list.next_playlist,
        keys.PREVIOUS_PLAYLIST_KEY: song_list.previous_playlist,
        keys.RANDOM_SONG_IN_PLAYLIST_KEY: song_list.random_song_in_playlist,
        keys.RANDOM_SONG_ANYWHERE_KEY: song_list.random_song_anywhere
    }

    print('Waiting for command: ')
    alive = True
    shutdown = False
    while alive and not shutdown:
        char = readchar.readchar()
        # Some systems return bytes. Other, strings.
        if not isinstance(char, str):
            char = char.decode('utf-8')
        char = char.upper()

        # Don't move to the next song automatically when processing a command
        with player.song_action_mutex:
            if char in song_transition_map:
                state = song_transition_map[char](state)
                _play_and_save(player, state)
            elif char == keys.PLAY_PAUSE_KEY:
                player.play_pause()
            elif char == keys.TOGGLE_EXCLUDED_GENRES_KEY:
                state.exclude_from_genre = not state.exclude_from_genre
                print("Excluding songs based on genre: {}".format(state.exclude_from_genre))
                if state.exclude_from_genre:
                    # TODO -- if this is an excluded genre song, or an excluded genre move to the next one
                    # Because of this, assume we cannot be on an excluded genre
                    # Or, on a non-excluded genre with only excluded songs
                    pass

                state.save()
            elif char == keys.QUIT_KEY:
                alive = False
            elif char == keys.SHUTDOWN_KEY:
                shutdown = True
            else:
                print('Unrecognized command "{}"'.format(char))

    player.terminate()
    _end_program()
