#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import json
import urllib2
import sys
from colorama import init
init()
from colorama import Fore

reload(sys)
sys.setdefaultencoding('utf-8')

token_file = os.path.join(os.path.expanduser("~"), '.whoislive-token')
clientid = "qr27075xc6n85gn944oj70qf0glly4" # please dont abuse

def streams(offset):
	url = "https://api.twitch.tv/kraken/streams/followed?client_id=" + clientid + "&oauth_token=" + token + "&stream_type=live&offset=" + str(offset) + "&limit=25"
	try:
		response = urllib2.urlopen(url)
		data = json.loads(response.read())
	except urllib2.HTTPError as err:
		if err.code == 401:
			print "Error 401: Unauthorized. Deleting your cached token. Run me again to get a new token."
			os.remove(token_file)
			sys.exit(1)
		elif err.code == 404:
			print "Error 404: Twitch is down?"
			sys.exit(1)
		else:
			print "Error: " + err
			sys.exit(1)

	for stream in data['streams']:
		#print stream
		name = stream['channel']['name']
		game = stream['game']
		status = stream['channel']['status']
		url = stream['channel']['url']
		viewers = str(stream['viewers'])
		print (Fore.GREEN + name),
		print (Fore.YELLOW + status), 
		print (Fore.RED + viewers  + " viewers")
	
	totalstreams = data['_total']
	return totalstreams



# Get token and save it if there is none
if not os.path.isfile(token_file):
	print "Please visit this URL to get a token: "
	print "https://api.twitch.tv/kraken/oauth2/authorize?response_type=token&client_id=qr27075xc6n85gn944oj70qf0glly4&scope=user_read&redirect_uri=http://lambdan.se/d/whoislive.html"
	print ""
	input_token = raw_input('Paste token here: ')

	print "Testing token..."
	testURL = "https://api.twitch.tv/kraken?client_id=" + clientid + "&oauth_token=" + input_token.rstrip()
	response = urllib2.urlopen(testURL)
	data = json.loads(response.read())
	if data["token"]["valid"] is True:
		print "Success! Hi " + data["token"]["user_name"]
		print "Saving token..."
		f = open(token_file,'w')
		f.write("token:" + input_token.rstrip())
		f.close()
	else:
		print "FAIL! Try running me again and we'll try to re-authenticate"
		sys.exit(1)

# We have a token, let's show who's live
if os.path.isfile(token_file):
	# Read token from file
	with open(token_file) as f:
		lines = f.readlines()
	token = lines[0].split(":")[1].rstrip()

	totalstreams = streams(0)  # get first 25 :) (yeah this is really weird structure wise but whatever)
	offset = 25
	while offset < totalstreams:
		streams(offset)
		offset += 25
