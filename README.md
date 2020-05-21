# whoislive

No need to visit your Twitch following page anymore. Useful for [streamlink](https://github.com/streamlink/streamlink) users.

![Demo](https://lambdan.se/img/2020-05-22_00-50-06.gif)

# Installation

No installation. Just download and run `whoislive.py` with Python 3.

I do require the [colorama](https://pypi.org/project/colorama/) package though, you can usually install that by just doing `pip3 install colorama`.

## Optional

I recommend setting up an alias in your shell, so you can just type `wil` anywhere to run it. For example I have `alias wil='python3 ~/whoislive.py'` in my `.zshrc`.

On Windows, you can create `wil.bat` which contains:

    @echo off
    call whoislive.py

... and then put `wil.bat` in [a folder that's in your `%PATH%`](https://github.com/lambdan/Setup/blob/master/Windows/Path%20Setup.md). Then you can simply type `wil` in any cmd or Powershell window and it will run.

# Troubleshooting

I'm using Windows, and after I double click the script and paste the token the window just closes?
- Because I finish executing my window gets closed. You should instead open a Command Prompt and run the script from there.

I want to switch Twitch account?
- Delete the saved token (currently it's saved to your home directory and it's called `.whoislive2-token`, just delete that file), then run me again.

I am not authenticated.
- First try deleting the saved token (see above) and try to re-authorize.
- If that still doesn't work Twitch likely changed their API again and I haven't noticed and updated the script for it. Please let me know if so.
