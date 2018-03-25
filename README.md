# whoislive 

No need to visit your Twitch following page anymore.
Useful for [streamlink](https://github.com/streamlink/streamlink) users.

![Regular version on macOS](http://i.imgur.com/Ysz5epa.png)

# What Version Should I Use?

The regular version is the original one that outputs in color and is meant to be ran inside a Terminal that supports colors. It requires the _colorama_ package to be installed. **Recommended for macOS Terminal users** and possibly Linux users, and maybe Windows users who got a good terminal...

The _no-color_ version is the same as the regular version, except there is no color and its output format is changed to make it more legible without color. **Recommended for Windows Command Prompt users** who add the script to their path.

The _noob_ version is the same as the _no-color_ version except it has a "Press any key to exit..." at the end. This is **recommended for beginners that use Windows** as you can just double click the `.py` file to run it. See the bottom of this readme for a demo.

All scripts use the same saved OAuth token, so you can use all versions at the same time.

# Installation

## _noob_ version

- Make sure Python 2.7 is installed (other versions untested)
	- Windows users can download it here: [Python 2.7](https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi)
	- On macOS it is already installed
- Download [whoislive-noob.py](https://github.com/lambdan/whoislive/raw/master/whoislive-noob.py)
- Double click the `.py` file you downloaded

## _no-color_ version

- Make sure Python 2.7 is installed (other versions untested)
	- Windows users can download it here: [Python 2.7](https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi)
	- On macOS it is already installed
- Download [whoislive-no-color.py](https://github.com/lambdan/whoislive/raw/master/whoislive-no-color.py)
- Recommended: Add it to your PATH (Windows) or add an alias to your `.bash_profile` (Unix) to make it accessible wherever you are
- Run the script in your Command Prompt/Terminal

## regular version

- Make sure Python 2.7 is installed (other versions untested)
	- Windows users can download it here: [Python 2.7](https://www.python.org/ftp/python/2.7.14/python-2.7.14.msi)
	- On macOS it is already installed
- Install Colorama: `pip install colorama`
- Download [whoislive.py](https://github.com/lambdan/whoislive/raw/master/whoislive.py)
- Recommended: Add it to your PATH (Windows) or add an alias to your `.bash_profile` (Unix) to make it accessible wherever you are
- Run the script in your Command Prompt/Terminal

# Re: Twitch Auth

It says I get access to your email, which I guess is true, but I haven't seen my own email while developing this, so I really don't. I guess "email" is Twitch's fancy wording for the `user_read` scope which I need to see who you are following.
(However the script runs client side so I don't see it anyway, and the `#access_token` is a hash so I don't see your oauth key in my web server logs either.)

tl;dr: I won't know anything about you

![Noob version usage](https://lambdan.se/d/whoislive-usage.gif)