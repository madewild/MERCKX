# 
# filter DBpedia labels by DBpedia places
# 

from sets import Set
import random
import urllib

# force UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# check command line arguments
langs = sys.argv[1:] or ['nl','fr']

# load list of places
places = Set()
with open('dbpedia-places.lst', 'r') as f:
	for line in f:
		places.add(line.strip()) # dbr:...

# load labels and check if place
labels = dict()
filenames = {'en':'labels_en.nt', 'fr':'labels_en_uris_fr.nt', 'nl':'labels_en_uris_nl.nt'}
nUpdate = 0
nConflict = 0
for lang in langs:
	filename = filenames[lang]
	print('Checking ' + lang.upper() + ' labels...')
	with open(filename, 'r') as inFile:
		for inLine in inFile:
			if inLine[0] == '#': # skip comment
				continue
			words = inLine.split() # split line into triple: uri rdfs:label "label"@fr .
			uri = words[0][1:-1].replace('http://dbpedia.org/resource/','dbr:') # <http://dbpedia.org/resource/base> => dbr:base
			# uri_label = urllib.unquote(uri[4:]).decode('utf8').replace('_',' ')
			label = ' '.join(words[2:-1])[1:-4].decode('unicode_escape') # "label"@fr => label
			if label in labels: # label already exist as place
				if uri == labels[label]: # same uri => OK
					pass
				elif uri in places: # new uri is a place => replace uri
					labels[label] = uri
					nUpdate += 1
				else: # new uri is not a place => remove confilected label
					del labels[label]
					nConflict += 1
			elif uri in places: # check if place
				labels[label] = uri

# write  labels of place in labels.lst 
# EN:731544  FR:187859  NL:194680  FR+NL:292629 NL+FR:293025 EN+FR+NL:881389 EN+NL+FR:881785 FR+NL+EN:851347 NL+FR+EN:851344
print('Writing dbpedia-labels.lst ...')
with open('dbpedia-labels.lst', 'w') as outFile:
	for label in labels:
		uri = labels[label]
		outLine = label + '\t' + uri + '\n'
		outFile.write(outLine) # write line to .lst file
print('{0:6d} labels with a different URI and the same (place) type have been updated'.format(nUpdate))
print('{0:6d} labels with a different URI and a different (place) type have been removed'.format(nConflict))
print('{0:6d} labels have been written to dbpedia-labels.lst'.format(len(labels.keys())))
