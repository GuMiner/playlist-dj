import psutil
import subprocess

import config


class Player:
    def __init__(self):
        self._current_player = None

    def stop_current_song(self):
        if self._current_player is not None:
            self._current_player.kill()
            self._current_player = None

    def play_pause(self):
        if self._current_player is not None:
            process = psutil.Process(self._current_player.pid)
            if process.status() == 'running':
                process.suspend()
            else:
                process.resume()

    def play(self, song_path):
        self.stop_current_song()
        print('  Playing "{}"'.format(song_path))

        args = [config.FFPLAY_TOOL_PATH, '-nodisp', '-loglevel', 'error', '-infbuf', '-autoexit', song_path]
        self._current_player = subprocess.Popen(args)