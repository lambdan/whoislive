# whoislive

No need to visit your Twitch following page anymore. Useful for [streamlink](https://github.com/streamlink/streamlink) users.

![terminal output](http://i.imgur.com/Ysz5epa.png)

# Installation

- Install Colorama: `pip3 install colorama`
- Download `whoislive.py`
  - Optional: I recommend setting up an alias in your shell, so you can just type `wil` anywhere to run it. For example I have `alias wil='python3 ~/whoislive.py'` in my [`.bash_profile`](https://github.com/lambdan/Setup/blob/master/Mac/Configs/.bash_profile)
  - On Windows, you can create `wil.bat` which contains:
  
        @echo off
        call whoislive.py
      
  ... and then put `wil.bat` in [a folder that's in your `%PATH%`](https://github.com/lambdan/Setup/blob/master/Windows/Path%20Setup.md). Then you can simply type `wil` anywhere.
  

# Usage

- Run `whoislive.py` using Python 3: `python3 whoislive.py` or use your alias
	- First run you will be asked to open a Twitch URL to authorize, and then you will be sent to a page that shows you a token code which you will copy/paste into _whoislive_, which will then be saved for future runs
		- If you want to switch Twitch account or your token expires, remove the token file (currently `~/.whoislive2-token`) and then run again to create a new token