# whoislive

No need to visit your Twitch following page anymore. Useful for [streamlink](https://github.com/streamlink/streamlink) users.

![terminal output](http://i.imgur.com/Ysz5epa.png)

# Installation

- Install Colorama: `pip3 install colorama`
- Download `whoislive.py`
- Optional: I recommend setting up an alias in your shell, so you can just type `wil` anywhere to run it. For example I have `alias wil='python3 ~/whoislive.py'` in my [`.bash_profile`](https://github.com/lambdan/Setup/blob/master/Mac/Configs/.bash_profile)

# Usage

- Run `whoislive.py` using Python 3: `python3 whoislive.py` or use your alias. 

- The first time you run it will ask for a Twitch username (preferably yours so you get who you are following, but you can type someone elses name to pretend to be them and see who they're following)
- Future runs will automatically show followed channels that are live for the username you previously specified
- If you want to change Twitch username, remove the token file (currently located at `~/.whoislive2-token`) and run again