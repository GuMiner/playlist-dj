import concurrent.futures
import subprocess

import config


def scan_files(files, progress):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(_scan_file, file, progress) for file in files]
        return [future.result() for future in futures]


def _scan_file(file_to_scan, progress):
    found_genres = _analyze_song(file_to_scan)

    progress.increment()
    return {'file': file_to_scan, 'genres': found_genres}


# Returns the genres a song is in or None if the path does not refer to a song
def _analyze_song(song_path):
    ignore_song_from_extension = any([song_path.upper().endswith(ext) for ext in config.KNOWN_FILETYPES_TO_IGNORE])
    if ignore_song_from_extension:
        print('      Ignoring "{}" from the extension.'.format(song_path))
        return None

    try:
        args = [config.EXIF_TOOL_PATH, '-Genre', song_path]
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        if result.returncode == 0:
            return _decode_genre_output(result.stdout)
        else:
            print('      exiftool returned {}: {}'.format(result.returncode, result.stdout))
            return None
    except Exception as e:
        print('      Could not parse "{}": {}'.format(song_path, str(e)))
        return None


def _decode_genre_output(stdout):
    # exiftool output should look like the following:
    # Genre                           : Instrumental/Smooth Jazz
    genres = stdout.split(':')[1].strip()
    genre_list = genres.split('/')
    return genre_list
