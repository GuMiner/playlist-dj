# playlist-dj
Queues up songs to play from metadata and accepts IR commands for remote control

# About
**playlist-dj** is a command-line media player that scans folders for songs, sorts them by genre, and plays them.

This player only accepts single characters as input, such as that sent by a remote control.

# Usage
```bash
python playlist_dj.py
```

Requires Python 3.7+

# Setup
The following instructions setup a Linux PC as a music player with IR remote control.

1. TODO -- add `ir-keytable` documentation here
2. Copy music to device
3. Install dependencies (TODO)
4. Update `config.py` with the keys setup in step 1
5. Setup this to run on boot with context (TODO)

# See Also
exiftool -- for getting song metadata

ffplay (provisionally) -- for playing songs