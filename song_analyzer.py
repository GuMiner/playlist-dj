import subprocess

import config


# Returns the genres a song is in or None if the path does not refer to a song
def analyze_song(song_path):
    try:
        args = [config.EXIF_TOOL_PATH, '-Genre', song_path]
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if result.returncode == 0:
            # exiftool output should look like the following:
            # Genre                           : Instrumental/Smooth Jazz
            genres = result.stdout.split(':')[1].strip()
            genre_list = genres.split('/')
            return genre_list
        else:
            raise ValueError('exiftool returned {}: {}'.format(
                result.returncode, result.stdout))
        pass
    except Exception as e:
        print('  Could not parse "{}": {}'.format(song_path, str(e)))
        return None
