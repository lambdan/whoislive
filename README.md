No need to visit your Twitch following page anymore

![terminal output](http://i.imgur.com/Ysz5epa.png)

# Installation

- Install Colorama: `pip install colorama`
- Download `whoislive.py`
- Add an alias to your `~/.bash_profile`, that looks something like this: `alias whoislive="python /path/to/whoislive.py"`

Only tested on macOS, Python 2.7

# Re: Twitch Auth

It says I get access to your email, which I guess is true, but I haven't seen my own email while developing this, so I really don't. I guess "email" is Twitch's fancy wording for the `user_read` scope which I need to see who you are following.
(However the script runs client side so I don't see it anyway, and the `#access_token` is a hash so I don't see your oauth key in my web server logs either.)

tl;dr: I won't know anything about you
