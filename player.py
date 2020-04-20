import subprocess

import config


class Player:
    def __init__(self):
        self.current_player = None

    def stop_current_song(self):
        if self.current_player is not None:
            self.current_player.kill()
            self.current_player = None

    def play(self, song_path):
        self._stop_current_song()
        print('    Playing "{}"'.format(song_path))

        args = [config.FFPLAY_TOOL_PATH, '-nodisp', '-loglevel', 'error', '-infbuf', '-autoexit', song_path]
        self.current_player = subprocess.Popen(args)