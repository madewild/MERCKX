#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib, urllib2, json
from urllib import unquote_plus as up
import re
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# set paramaters
delay = 3 # delay between API calls
filetype = sys.argv[1] if len(sys.argv) > 1 else 'raw'
if filetype not in ['raw', 'corr']:
	print("usage: {0} raw or corr".format(sys.argv[0]))
	sys.exit()
if filetype == 'raw':
	inFilename = "gsc3.txt"
	outFilename = "raw-Zemanta-ent.mapped"
else:  
	inFilename = "gsc3.new.txt"
	outFilename = "corr-Zemanta-ent.mapped"

# extract places entities from Zemanta service
def get_entities(text,offset):
	global places
	url = "http://papi.zemanta.com/services/rest/0.0/"
	values = {'api_key' : '4eqem8kyjzvkz8d2ken3xprb',
					'return_rdf_links' : 1,
					'method' : 'zemanta.suggest_markup',
					'format' : 'json',
					'text' : text }
	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	page = response.read()
	j = json.loads(page)
	s = set()
	if j['status']=='ok':
		entities = j['markup']['links']
		for e in entities:
			a = e['anchor']
			candidates = e['target']
			for c in candidates:
				if 'dbpedia' in c['url']:
					uri = c['url'].replace("http://dbpedia.org/resource/", "dbr:")
					if uri in places:
						positions = [(m.start(),m.end()) for m in re.finditer(a, text)]
						for pos in positions:
							start = pos[0]
							stop = pos[1]
							s.add((offset+start,offset+stop,up(str(uri[4:])))) # dbr:...
		for m in sorted(s):
			a,z,e = m
			print("{0}\t{1}\t{2}\t{3}".format(inFilename, a, z, e))
	else:
		print "Error:",j['status']
	return s

# load DBpedia places
places = set()
with open("dbpedia-places.lst") as locs:
	for uri in locs:
		places.add(uri.strip())

# collect results
offset = 0
results = set()
with open(inFilename) as inFile:
	for line in inFile:
		text = line.decode('utf-8')
		results = results.union(get_entities(text,offset))
		offset += len(text)
		time.sleep(delay)

# write results
with open(outFilename, 'w') as outFile:
	for item in sorted(results):
		(start, stop, label) = item
		outFile.write("{0}\t{1}\t{2}\t{3}\n".format(inFilename, start, stop, label))

