import psutil
import subprocess
import time
import threading

import config


class Player:
    _current_player: subprocess.Popen

    def __init__(self, next_song_callback):
        self._current_player = None
        self._next_song_callback = next_song_callback
        self.song_action_mutex = threading.Semaphore(value=1)

        self._alive = True
        self._watcher_thread = threading.Thread(target=self._next_song_watcher)
        self._watcher_thread.start()

    def _next_song_watcher(self):
        while self._alive:
            with self.song_action_mutex:
                if self._current_player is not None:
                    if self._current_player.poll() is not None:
                        self._next_song_callback()
            time.sleep(0.1)

    def terminate(self):
        self._alive = False
        self.stop_current_song()

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