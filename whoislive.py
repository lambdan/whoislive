#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os.path
import json
try:
    raw_input = raw_input
except NameError:
    raw_input = input
try:
    # python3 fixes
    import urllib.request as urllib2
except ImportError:
    import urllib2
import sys
from colorama import Fore
from colorama import init
init()

try:
    reload
except NameError:
    # python3 has unicode by default
    pass
else:
    reload(sys).setdefaultencoding('utf-8')


token_file = os.path.join(os.path.expanduser("~"), '.whoislive2-token')
clientid = "qr27075xc6n85gn944oj70qf0glly4"  # please dont abuse


# Get token and save it if there is none
if not os.path.isfile(token_file):
    input_username = raw_input('Enter your Twtich.tv username (or someone elses if you wanna pretend to be them): ')

    print("Grabbing User ID...")
    req = urllib2.Request('https://api.twitch.tv/helix/users?login=' + input_username)
    req.add_header('Client-ID', clientid)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    if len(data['data']) == 1:
        print("Username: " + data['data'][0]['login'])
        print("Saving user id to " + token_file + "...")
        f = open(token_file, 'w')
        f.write("username:" + data['data'][0]['login'])
        f.write("\n")
        f.write("userid:" + data['data'][0]['id'])
        f.close()
    else:
        print('FAILED!')
        print('This could be because of:')
        print('- User does not exist')
        print('- Twitch changed their API')
        print('- Or something weird just happened...')
        print('Try again if you want to.')
        sys.exit(1)

# We have a token file, read userid 
if os.path.isfile(token_file):
    # Read token from file
    with open(token_file) as f:
        lines = f.readlines()
    for l in lines:
        if l.split(":")[0] == 'userid':
            userid = l.split(":")[1].rstrip()
            #print("DEBUG: user id: " + str(userid))

# We got the user id, now lets show who's live
if userid:
    # grab followed streams
    req = urllib2.Request('https://api.twitch.tv/helix/users/follows?from_id=' + userid + '&first=100')
    req.add_header('Client-ID', clientid)
    response = urllib2.urlopen(req)
    data = json.loads(response.read())
    
    # figure out total amount of channels
    followed_channels = []
    total = int(data['total'])
    #print ('Followed channels:', total)

    # iterate follows
    for channel in data['data']:
        #print (channel['to_name']) # to_id to_name
        followed_channels.append(channel['to_id'])

    if total > 100: # we need pagination
        while len(followed_channels) < total:
            pagination_cursor = data['pagination']['cursor']
            #print ('DEBUG pagination cursor:', pagination_cursor)
            req = urllib2.Request('https://api.twitch.tv/helix/users/follows?from_id=' + userid + '&first=100&after=' + pagination_cursor)
            req.add_header('Client-ID', clientid)
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            for channel in data['data']:
                #print (channel['to_name']) # to_id to_name
                followed_channels.append(channel['to_id'])

    # validate follows to make sure there are no dupes because i dont trust my pagination skills
    if len(followed_channels) != total:
        print ("error! amount of parsed channels and followed channels reported from twitch do not match")
        sys.exit(1)

    for c in followed_channels:
        if followed_channels.count(c) > 1:
            print ("error! duplicate in followed channels:",c)
            sys.exit(1)


    #print ('DEBUG: len fc list:', len(followed_channels))

    # generate urls that we will call to see who is live
    # we need to do this because you can request max 100 channels per call
    # this is a damn mess btw
    urls_to_call = []
    x = 0
    while x < len(followed_channels):
        i = 0
        url = 'https://api.twitch.tv/helix/streams?'
        while i < 100: # 100 per call
            if i > 0:
                url += "&" # the first user_id= uses the ? in /streams?
            url += 'user_id=' + followed_channels[x]
            i += 1
            x += 1
            if x == len(followed_channels): # we've gone through all channels
                break
        urls_to_call.append(url)
            
    #print ('debug x ', x) # should be the same as total and len(followed_channels)

    # now call the urls and get who is actually live
    live_channels = []
    for url in urls_to_call:
        req = urllib2.Request(url)
        req.add_header('Client-ID', clientid)
        response = urllib2.urlopen(req)
        data = json.loads(response.read())
        for channel in data['data']:
            #print(channel['user_name'])
            live_channels.append({'user': channel['user_name'], 'title': channel['title'], 'viewers': channel['viewer_count']})

    #print ('Live channels:', len(live_channels))

    # sort by most viewers 
    live_channels_sorted_by_viewers = sorted(live_channels, key=lambda k: k['viewers'], reverse=True)

    # print output if there are live channels
    if len(live_channels) > 0:
        for channel in live_channels_sorted_by_viewers: # user, title, viewers
            print (Fore.GREEN + channel['user'], Fore.YELLOW + channel['title'], Fore.RED + str(channel['viewers']))
    else:
        print("No one you follow is live :(")