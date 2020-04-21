import asyncio
import asyncio.subprocess
import sys

import config

process_limiter = None


def set_process_limiter(limit=20):
    global process_limiter
    process_limiter = asyncio.Semaphore(limit)


def allow_subprocess_in_asyncio():
    if sys.platform == 'win32':
        # https://bugs.python.org/issue33792 yay Python async/await on Windows bug...
        policy = asyncio.get_event_loop_policy()
        policy._loop_factory = asyncio.ProactorEventLoop


def _decode_genre_output(stdout):
    # exiftool output should look like the following:
    # Genre                           : Instrumental/Smooth Jazz
    genres = stdout.split(':')[1].strip()
    genre_list = genres.split('/')
    return genre_list


# Returns the genres a song is in or None if the path does not refer to a song
async def analyze_song(song_path):
    ignore_song_from_extension = any([song_path.upper().endswith(ext) for ext in config.KNOWN_FILETYPES_TO_IGNORE])
    if ignore_song_from_extension:
        print('      Ignoring "{}" from the extension.'.format(song_path))
        return None

    try:
        async with process_limiter:
            exiftool_process = await asyncio.create_subprocess_exec(
                config.EXIF_TOOL_PATH, '-Genre', song_path,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
            stdout, _ = await exiftool_process.communicate()

        stdout = stdout.decode(encoding='UTF8')
        exit_code = exiftool_process.returncode
        if exit_code == 0:
            return _decode_genre_output(stdout)
        else:
            print('      exiftool returned {}: {}'.format(exit_code, stdout))
            return None
    except Exception as e:
        print('      Could not parse "{}": {}'.format(song_path, str(e)))
        return None
