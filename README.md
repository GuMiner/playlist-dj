# playlist-dj
Queues up songs to play from metadata and accepts IR commands for remote control.

# About
**playlist-dj** is a command-line media player that scans folders for songs, sorts them by genre, and plays them.

This player only accepts single characters as input, such as that sent by a remote control.

# Usage
```bash
python playlist_dj.py
```

Requires Python 3.7+

# Setup
The following instructions setup a PC as a music player with IR remote control.

1. Setup the remote control to generate keypresses
- Linux
  > sudo apt-get install ir-keytable
          
  > TODO continue instructions
- Windows
  > C
2. Copy music to the device
3. Install dependencies
```
    sudo apt-get install exiftool ffmpeg python3.7 python3.7-dev
    python3.7 -m pip install readchar psutil
```
4. Update `config.py` with the keys setup in step 1, if you customized any of the buttons
5. Setup this to run on boot with context (TODO)
- Run with `python3.7 playlist_dj.py`

# See Also
[exiftool](https://exiftool.org/) -- to extract song genres from metadata

[ffplay](https://ffmpeg.org/ffplay.html) -- to play songs