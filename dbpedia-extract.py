# 
# filter DBpedia labels by DBpedia places
# 

from sets import Set
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# load list of places
places = Set()
with open('dbpedia-places.lst', 'r') as f:
	for line in f:
		places.add(line.strip()) # dbr:...

# extract labels (FR:942506=>187859, NL:674849=>194680)
for lang in ('fr', 'nl'):
	print('--- Extracting DBpedia ' + lang.upper() + ' labels...')
	inFilename = 'labels_en_uris_' + lang + '.nt'
	outFilename = inFilename.replace('.nt','.lst')
	with open(outFilename, 'w') as outFile:
		with open(inFilename, 'r') as inFile:
		  for inLine in inFile:
		  	# triple: uri rdfs:label "label"@fr .
		  	words = inLine.split()
		  	uri = words[0].replace('http://dbpedia.org/resource/','dbr:').replace('<','').replace('>','') # http://dbpedia.org/... => dbr:...
		  	# save label <tab> uri if uri is a place
		  	if uri in places:
			  	label = ' '.join(words[2:-1]).replace('"','').replace('@'+lang,'').decode('unicode_escape') # "label"@fr => label
		  		outLine = label + '\t' + uri + '\n'
		  		# write line to .lst file
		  		outFile.write(outLine)
