#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Create MERCKX data files from DBpedia 2014 dataset called from merckx-init.sh'''

import os
import sys

# parameters
LABEL_MAX_LENGTH = 40 # maximum number of characters per label

# check command line arguments
langs = [lang.upper() for lang in sys.argv[1:]] or ['EN', 'NL', 'FR']
entityTypes = ['Place']

# load entities
entities = {}
for entityType in entityTypes:
    entities[entityType] = set() # initialize lists
if os.path.isfile('data/entities_Place.lst'):
    print('***  Loading list of entities...')
    for entityType in entityTypes:
        filename = 'data/entities_'+entityType+'.lst'
        with open(filename, 'r') as inFile:
            entities[entityType] = set((inFile.read()).strip().split('\n'))
        print('--- {0:8d} {1}s'.format(len(entities[entityType]), entityType.lower()))
else:
    print('*** Building list of entities...')
    with open('dbpedia/instance_types_en.nt', 'r') as inFile:
        for line in inFile:
            line = line.strip()
            if line[0:1] in ['', '#']: # skip empty or # comment line
                continue
            triple = line.split(' ')
            uri = triple[0][1:-1].replace('http://dbpedia.org/resource/', 'dbr:') # <http://dbpedia.org/resource/name> => dbr:name
            # p is <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> (rdf:type)
            entityType = triple[2][1:-1].replace('http://dbpedia.org/ontology/', '') # <http://dbpedia.org/ontology/type> => type
            if entityType in entityTypes:
                entities[entityType].add(uri)
    for entityType in entityTypes: # save optimized lists
        filename = 'data/entities_'+entityType+'.lst'
        with open(filename, 'w') as outFile: # save optimized list
            for key in sorted(entities[entityType]):
                outFile.write(key+'\n')
        print('--- {0:8d} {1}s'.format(len(entities[entityType]), entityType.lower()))

# filter list of labels per language and entityType
print('*** Building list of labels...')
labels = {}
for entityType in entityTypes:
    labels[entityType] = {}
upd_uris = 0
del_uris = 0
for lang in langs: # scan all labels per language and filter per entityType
    filename = 'dbpedia/labels_en.nt' if lang == 'EN' else 'dbpedia/labels_en_uris_'+lang.lower()+'.nt'
    with open(filename, 'r') as inFile: # read labels_*.nt
        countLine = 0
        for line in inFile:
            line = line.strip()
            if line[0:1] in ['', '#']: # skip empty or # comment line
                continue
            countLine += 1
            triple = line.split(' ') # split line into spo (triple): uri rdfs:label "label"@fr .
            uri = triple[0][1:-1].replace('http://dbpedia.org/resource/', 'dbr:') # <http://dbpedia.org/resource/base> => dbr:base
            label = ' '.join(triple[2:-1])[1:-4].decode('unicode_escape') # "label"@fr => label
            if len(label) > LABEL_MAX_LENGTH: # do not process label larger than 40 characters
                continue
            for entityType in entityTypes:
                if label in labels[entityType]: # label already exists
                    if uri == labels[entityType][label]: # same uri
                        pass
                    elif uri in entities[entityType]: # uri is an entity => save uri
                        labels[entityType][label] = uri
                        upd_uris += 1
                    else: # uri is not an entity => remove entry
                        del labels[entityType][label]
                        del_uris += 1
                elif uri in entities[entityType]: # uri is an entity => save uri
                    labels[entityType][label] = uri
                else:
                    pass
        print('--- {0:8d} labels ({1})'.format(countLine, lang.upper()))
print(upd_uris)
print(del_uris)

# save labels per entityType into 'labels-<entityType>.lst'
print('***  Writing list of labels...')
for entityType in entityTypes:
    filename = 'data/labels_'+entityType+'.lst'
    print('--- {0:8d} {1}s'.format(len(labels[entityType]), entityType.lower()))
    with open(filename, 'w') as outFile:
        # for label, uri in labels[entityType].iteritems():
        #     outFile.write(label.encode('utf8')+'\t'+uri+'\n')
        for label in sorted(labels[entityType]):
            uri = labels[entityType][label]
            outFile.write(label.encode('utf8')+'\t'+uri+'\n')
