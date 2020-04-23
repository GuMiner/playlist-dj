# playlist-dj
Queues up songs to play from metadata and accepts IR commands for remote control.

# About
**playlist-dj** is a command-line media player that scans folders for songs, sorts them by genre, and plays them.

This player only accepts single characters as input, such as that sent by a remote control.

# Usage

1. Configure (see **Setup**) 
2. Run ```python playlist_dj.py```

# Setup
## Music
Add a genre to the 'Genre' tag of each song.
> To add multiple genres, add a '/' between each separate genre.

If on Windows, you can use [Music Bee](https://getmusicbee.com/) and use the 'Genres' field for each song.
> MusicBee will automatically add in a '/' between separate genres. 

## Hardware
### Linux
Follow the instructions [here](https://madaboutbrighton.net/articles/2015/remote-control-media-player-without-lirc-using-ir-keymap)
to map each remote keypress to a button.
> See **config\keys.py** for the keys expected by this program. You can update **keys.py** if you want a different key to perform a different function. 

### Windows
I don't have a PC with an IR receiver for Windows, so you'll have to find instructions yourself for this step.

Please file a PR with improvements if you set this program up for Windows.

## Software
1. Update `config\environment.py` with your own values for `SONG_FOLDER`, `EXIF_TOOL_PATH`, and `FFPLAY_TOOL_PATH` 
2. Copy music to the device
3. Install dependencies
    ```bash
    sudo apt-get install exiftool ffmpeg python3.7 python3.7-dev supervisor
    python3.7 -m pip install readchar psutil
    ```
4. Run with `python3.7 playlist_dj.py`

## (Optional) Start-on-boot
To setup **playlist-dj** to start on boot, follow [these instructions](https://askubuntu.com/questions/308581/how-to-launch-terminal-on-login)

# See Also
[exiftool](https://exiftool.org/) -- to extract song genres from metadata

[ffplay](https://ffmpeg.org/ffplay.html) -- to play songs