import os.path
import json
import urllib.request as urllib2
import sys

token_file = os.path.join(os.path.expanduser("~"), '.whoislive2-token')
clientid = "qr27075xc6n85gn944oj70qf0glly4"  # please dont abuse
redirect = 'http://lambdan.se/d/whoislive.html'

def TwitchRequest(url, oauth_token):
    #print("TwitchRequest:", url)
    req = urllib2.Request(url)
    req.add_header('Client-ID', clientid)
    req.add_header('Authorization', 'Bearer ' + oauth_token)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        print("Error contacting Twitch:", e, "\nMaybe your internet is down or Twitch is having problems?")
        if "401" in str(e):
            print("Or maybe your token has expired. Would you like to remove it to re-authorize?")
            answer = input("Delete old token (y/n)? ")
            if "y" in answer.lower():
                os.remove(token_file)
                if not os.path.isfile(token_file):
                    print("OK, token deleted. Next time you run me we'll re-authorize.")
                else:
                    print("Error deleting token. Remove it yourself:", token_file)
        sys.exit(1)
    data = json.loads(response.read().decode("utf8"))
    return data

# Get token and save it if there is none
if not os.path.isfile(token_file):
    print("Please visit this URL to get a token: ")
    print("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=" + clientid + "&scope=user%3Aread%3Afollows&redirect_uri=" + redirect + "&force_verify=true")
    print("")
    input_token = input('Paste token here: ')

    print("Testing...")
    data = TwitchRequest('https://api.twitch.tv/helix/users', input_token.rstrip())
    if len(data['data']) == 1:
        print("Hello " + data['data'][0]['login'] + "!")
        print("Saving to " + os.path.abspath(token_file) + "...\n\n")
        f = open(token_file, 'w')
        f.write("username:" + data['data'][0]['login'])
        f.write("\n")
        f.write("userid:" + data['data'][0]['id'])
        f.write("\n")
        f.write("oauth:" + input_token.rstrip())
        f.close()
    else:
        print('FAILED!')
        print('This could be because of:')
        print('- User does not exist')
        print('- Twitch changed their API')
        print('- Or something weird just happened...')
        print('Try again if you want to.')
        sys.exit(1)

# We have a token file, read userid from it
if os.path.isfile(token_file):
    with open(token_file) as f:
        lines = f.readlines()
    for l in lines:
        if l.split(":")[0] == 'userid':
            userid = l.split(":")[1].rstrip()
        elif l.split(":")[0] == 'oauth':
            token = l.split(":")[1].rstrip()


# We got the user id, now lets show who's live
if userid:
    # Grab followed streams
    data = TwitchRequest('https://api.twitch.tv/helix/channels/followed?user_id=' + userid + '&first=100', token)
    #print(data)
    
    # Check total amount of channels
    total = int(data['total'])
    #print ('Followed channels according to Twitch:', total)

    # Iterate follows
    followed_channels = []
    for channel in data['data']:
        followed_channels.append(channel['broadcaster_id'])

    if total > 100: # we need pagination
        while len(followed_channels) < total:
            pagination_cursor = data['pagination']['cursor']
            data = TwitchRequest('https://api.twitch.tv/helix/channels/followed?user_id=' + userid + '&first=100&after=' + pagination_cursor, token)
            for channel in data['data']:
                followed_channels.append(channel['broadcaster_id']) # Add channel id to followed_channels

    # Generate urls that we will later call to see who is live
    urls_to_call = []
    i = 1
    url = 'https://api.twitch.tv/helix/streams?'
    for channel in followed_channels:
        url += 'user_id=' + channel
        if i == 100: # max 100 per call
            urls_to_call.append(url)
            url = 'https://api.twitch.tv/helix/streams?'
            i = 1
        elif channel == followed_channels[-1]: # Last channel. This is so we won't end the url with an &
            urls_to_call.append(url)
            break
        else:
            url += '&'
            i += 1

    # Now call the urls and get who is actually live
    live_channels = []
    for url in urls_to_call:
        data = TwitchRequest(url, token)
        #print(data)
        for channel in data['data']:

            if channel['user_name'].lower() == channel['user_login'].lower():
                display_name = channel['user_name']
            else:
                # for kanji/asian usernames: also show the user_login
                display_name = channel['user_name'] + " (" + channel['user_login'] + ")" 

            live_channels.append({'user': channel['user_login'], 'display_name': display_name, 'game': channel['game_name'], 'title': channel['title'], 'viewers': channel['viewer_count']})

    #print ('Live channels:', len(live_channels))

    # Sort by most viewers 
    live_channels_sorted_by_viewers = sorted(live_channels, key=lambda k: k['viewers'], reverse=True)

    # Output if there are live channels
    if len(live_channels) > 0:
        for channel in live_channels_sorted_by_viewers: # user, title, viewers
            pre_title = channel['display_name'] + " [" + str(channel['viewers']) + "] "
            title_length = 80 - len(pre_title) # max title length, 80 is common for terminals

            if len(channel['title']) > title_length:
                display_title = channel['title'][0:title_length-3] + "..."
            else:
                display_title = channel['title']
            
            display_title = display_title.replace("\n","")
            print(pre_title + display_title)

    else:
        print("No one you follow is live :(")
