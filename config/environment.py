import sys

DEPLOYMENT_ENVIRONMENT = 'Windows' if sys.platform == 'win32' else 'Linux'


def is_linux():
    return DEPLOYMENT_ENVIRONMENT == 'Linux'


SONG_FOLDER = '/home/guminer/Music' if is_linux() else r'C:\Users\Gustave\Music'

EXIF_TOOL_PATH = '/usr/bin/exiftool' if is_linux() else r'C:\Users\Gustave\AppData\Local\Programs\ExifTool\ExifTool.exe'
FFPLAY_TOOL_PATH = '/usr/bin/ffplay' if is_linux() else r'C:\users\gustave\desktop\programs\ffmpeg\bin\ffplay.exe'
