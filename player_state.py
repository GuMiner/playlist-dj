import json

from config import song_db


class PlayerState:
    def __init__(self, genre, song_path, exclude_from_genre):
        self.genre = genre
        self.song_path = song_path
        self.exclude_from_genre = exclude_from_genre

    def save(self):
        try:
            state = {'genre': self.genre, 'song_path': self.song_path, 'exclude_from_genre': self.exclude_from_genre}
            with open(song_db.LAST_PLAYER_STATE_FILE, 'w+') as json_file:
                json.dump(state, json_file)
        except Exception as e:
            print('  Failed to save player state: {}'.format(str(e)))

    @classmethod
    def from_saved_state(cls):
        try:
            with open(song_db.LAST_PLAYER_STATE_FILE, 'r') as json_file:
                data = json.load(json_file)
                return cls(data['genre'], data['song_path'], data['exclude_from_genre'])
        except FileNotFoundError:
            print('  Could not read player state. Playing a random file instead.')
        except Exception as e:
            print('  Failed to read player state: {}'.format(str(e)))
            return None
