#!/usr/bin/python
# -*- coding: utf-8 -*-
#recreate podcast feed, cleaned up so it'll be accepted by itunes.

import os, sqlite3 as lite
from datetime import datetime
from flask import Flask, render_template, request, json, abort, make_response, jsonify, Blueprint, redirect, url_for, session, Response
from werkzeug.contrib.atom import AtomFeed
from feedgen.feed import FeedGenerator

#itunes_keywords='''<itunes:keywords>OpenDoor,Walnut,Creek,Oakland,East,Bay,Jesus,Jer,Swigart,Dave,Kludt,Elizabeth,Hunnicutt,Way,of,Jesus</itunes:keywords>'''
#<guid isPermaLink="true">URL</guid>

#app = Flask(__name__)
app = Flask(__name__, static_url_path='')
#application = Flask(__name__)
application = Flask(__name__, static_url_path='')
db = 'podcast.db'
base_url = 'http://www.opendooreastbay.com/'

def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d

def feedgen():
	with lite.connect(db) as conn:
		conn.row_factory = dict_factory
		#conn.row_factory = lite.Row
		query = ("select * from podcast_items order by id DESC;")
		cursor = conn.cursor()
		cursor.execute(query)
		data = cursor.fetchall()
		# now process to xml:
		
		fg = FeedGenerator()
		fg.title('Teaching Podcast - Open Door')
		fg.description('''We are a family of sojourners learning to walk in the way of Jesus for the good of the world (www.opendooreastbay.com)''')
		fg.load_extension('podcast')
		fg.language('en-US')
		fg.link(href='http://ec2-54-149-239-188.us-west-2.compute.amazonaws.com/', rel='self', type="application/rss+xml")
		fg.podcast.itunes_author('Open Door East Bay')
		fg.podcast.itunes_category('Religion & Spirituality')
		fg.podcast.itunes_image('http://static1.squarespace.com/static/54c9a274e4b0d8961be0d970/t/555bb45ee4b051f7c699813d/1436299699944/1500w/od-emblem-blue.jpg')
		fg.podcast.itunes_subtitle('Open Door Teachings')
		fg.podcast.itunes_summary('''We are a family of sojourners learning to walk in the way of Jesus for the good of the world (www.opendooreastbay.com)''')
		fg.podcast.itunes_explicit('no')
		fg.podcast.itunes_owner(name='Open Door East Bay', email='info@opendooreastbay.com')

		fg.link(href='http://www.opendooreastbay.com', rel='alternate')
		for item in data:
			fe = fg.add_entry()
			fe.id(item['enclosure_url'])
			fe.podcast.itunes_author(item['itunes_author'])
			fe.podcast.itunes_subtitle(item['itunes_subtitle'])
			fe.podcast.itunes_explicit(item['itunes_explicit'])
			fe.podcast.itunes_image(item['itunes_image'])
			fe.podcast.itunes_duration(item['itunes_duration'])
			fe.link(href=item['link'], rel='enclosure')
			fe.title(item['title'])
			fe.description(item['itunes_subtitle'])
			fe.enclosure(item['enclosure_url'], item['enclosure_length'], item['enclosure_type'])
		fg.rss_str(pretty=True)
		fg.rss_file('podcast.xml')
		print "wrote xml!"
		return "wrote xml!"
	#return Response(fg.rss_file('podcast.xml'),mimetype='text/xml')
	#return Response('podcast.xml', mimetype='text/xml')
		

@app.route('/')
@app.route('/feed')
@app.route('/feed/')
def serve():
	print "getting fresh xml"
	feedgen()
	print "reading xml"
	with open('podcast.xml', 'r') as myfile:
		data=myfile.read()
	return data, 200, {'Content-Type': 'text/xml; charset=utf-8'}

if __name__ == '__main__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)
