#!/usr/bin/python
# -*- coding: utf-8 -*-

#parse xml/rss feed and write to sql

import xmltodict, re, requests, os, urllib, time, sqlite3 as lite
from requests import get
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup
from sys import argv
from mutagen.mp3 import MP3

url = '''http://www.opendooreastbay.com/podcast?format=rss'''
#http://feeds.feedburner.com/OpenDoorEastBay

def download_xml(url): #download file
	for x in range(10): # try 10 times, ftp server disconnects often in testing.
		print "Attempt #%s" % str(int(x)+1)
		if x > 0:
			print "Waiting 30 seconds before trying again."
			time.sleep(30)
		try:
			chunk_size = 2048
			r = requests.get(url)
			if r.status_code == '200':
				with open(xml_file, 'wb') as file:
					file.write(r.content)
				return str(xml_file)
				break
		except:
			print "Failed to connect to FTP 10 times, exiting."
			return False

def var(var,x): #set variable, but default to none
	try:
		var=x
		return var
	except:
		return None

def audio_length(url):
	urllib.urlretrieve(URL, "filename")
	print "Download Complete!"
	audio = MP3("example.mp3")
	print audio.info.length

def parse_channel(rssFeed): #channel elements
	for channel in rssFeed['rss']['channel']:
		try: channelTitle = channel['title']
		except: channelTitle = None
		try: channelLink = channel['link']
		except: channelLink = None
		try: channelBuildDate = channel['lastBuildDate']
		except: channelBuildDate = None
		try: channelLanguage = channel['language']
		except: channelLanguage = None
		try: channelGenerator = channel['generator']
		except: channelGenerator = None
		try: channelAuthor = channel['itunes:author']
		except: channelAuthor = None
		try: channelSubtitle = channel['itunes:subtitle']
		except: channelSubtitle = None
		try: channelSummary = channel['itunes:summary']
		except: channelSummary = None
		try: channelDescription = channel['description']
		except: channelDescription = None
		try: channelExplicit = channel['itunes:explicit']
		except: channelExplicit = None
		try: channelKeywords = channel['itunes:keywords']
		except: channelKeywords = None
		try: channelOwner = channel['itunes:owner']
		except: channelOwner = None
		try: channelNewFeed = channel['itunes:new-feed-url']
		except: channelNewFeed = None
		try: channelCategory = channel['itunes:category']
		except: channelCategory = None
		try: channelImage = channel['itunes:image']
		except: channelImage = None

def parse_items(rssFeed):
	item_dict = {}
	for item in rssFeed['rss']['channel']['item']:
		item_dict = {}
		try: title = item['title']
		except: title = None	
		item_dict['title']=title
		try: dc_creator = item['dc:creator']
		except: dc_creator = None
		item_dict['dc_creator']=dc_creator
		try: pubDate = item['pubDate']
		except: pubDate = None
		item_dict['pubDate']=pubDate
		try: link = item['link']
		except: link = None
		item_dict['link']=link	
		try: guid = item['guid']
		except: guid = None
		try: itunes_author = item['itunes:author']
		except: itunes_author = None	
		item_dict['itunes_author']=itunes_author
		try: itunes_subtitle = item['itunes:subtitle']
		except: itunes_subtitle = None	
		item_dict['itunes_subtitle']=itunes_subtitle
		try: itunes_explicit = item['itunes:explicit']
		except: itunes_explicit = None
		item_dict['itunes_explicit']=itunes_explicit
		try: itunes_duration = item['itunes:duration']
		except: itunes_duration = '00:30:00'
		item_dict['itunes_duration']=itunes_duration
		try: itunes_image = item['itunes:image']['@href']
		except: itunes_image = None	
		item_dict['itunes_image']=itunes_image
		try: enclosure_url = item['enclosure']['@url']
		except: enclosure_url = None
		item_dict['enclosure_url']=enclosure_url
		item_dict['guid']=enclosure_url

		try: enclosure_length = item['enclosure']['@length']
		except: enclosure_length = None
		item_dict['enclosure_length']=enclosure_length
		try: enclosure_type = item['enclosure']['@type']
		except: enclosure_type = None
		item_dict['enclosure_type']=enclosure_type
		log_item(item_dict)

def log_item(item_dict):
	conn = None
	columns = ', '.join(item_dict.keys())
	placeholders = ':'+', :'.join(item_dict.keys())
	try: 
		with lite.connect(db) as conn:
			query = 'INSERT INTO podcast_items (%s) VALUES (%s)' % (columns, placeholders)
			cursor = conn.cursor()
			cursor.execute(query, item_dict)
			conn.commit()
	except:
		pass

def check_db(db,schema_filename):
	if not os.path.exists(db):
		with lite.connect(db) as conn:
			print 'Creating schema'
			with open(schema_filename, 'rt') as f:
				schema = f.read()
			conn.executescript(schema)

def count_items():
	with lite.connect(db) as conn:
			query = '''select count(*) as 'count' from podcast_items;'''
			cursor = conn.cursor()
			cursor.execute(query)
			data = cursor.fetchall()
			print data

##########
###CODE###
##########
schema = 'podcast_schema.sql'
db = 'podcast.db'
xml_file = 'feed.xml'
#xml_file = download_xml(url) # seems broken, switch to wget/curl cronjob

check_db(db,schema)

if xml_file:
	with open(xml_file) as fd:
		rssFeed = xmltodict.parse(fd.read())

	parse_channel(rssFeed)

	parse_items(rssFeed)

	count_items()

rssFeed = None
exit()
