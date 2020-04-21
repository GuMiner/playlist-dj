import json

import config


class PlayerState:
    def __init__(self, genre, song_path):
        self.genre = genre
        self.song_path = song_path

    def save(self):
        try:
            state = {'genre': self.genre, 'song_path': self.song_path}
            with open(config.LAST_PLAYER_STATE_FILE, 'w+') as json_file:
                json.dump(state, json_file)
        except Exception as e:
            print('  Failed to save player state: {}'.format(str(e)))

    @classmethod
    def from_saved_state(cls):
        try:
            with open(config.LAST_PLAYER_STATE_FILE, 'r') as json_file:
                data = json.load(json_file)
                return cls(data['genre'], data['song_path'])
        except FileNotFoundError:
            print('  Could not read player state. Playing a random file instead.')
        except Exception as e:
            print('  Failed to read player state: {}'.format(str(e)))
            return None
