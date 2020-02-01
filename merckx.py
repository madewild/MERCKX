#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib
from urllib.parse import unquote_plus as up
from nltk.tokenize import WordPunctTokenizer as tokenizer

# from jellyfish import levenshtein_distance as ld
# to add support for clustering

# check parameters
txtType = sys.argv[1].upper() if len(sys.argv) > 1 else ''
txtFilename = sys.argv[2] if len(sys.argv) > 2 else ''
entityTypes = {'EVE':'Event', 'LOC':'Place', 'PER':'Person', 'ORG':'Organisation'}
if txtType not in entityTypes or not os.path.isfile(txtFilename):
    print("Syntax: merckx.py <type> <filename>")
    print("where   <type> is the entity type: EVE LOC PER ORG")
    print("and     <filename> is the name of text file to analyze")
    print
    sys.exit(0)

# load labels of entities
labels = {}
entityType = entityTypes[txtType]
filename = 'data/labels_'+entityType+'.lst'
with open(filename, 'rb') as inFile:
    lines = inFile.read().decode('utf8').strip().split('\n')
    for line in lines:
        label, uri = line.split('\t')
        labels[label] = uri

# load + tokenize + extract entities from text file
source = os.path.basename(txtFilename)
text = open(txtFilename, 'rb').read().decode('utf8')
tokens = tokenizer().tokenize(text) # list of tokens from NLTK Tokenizer
pos = list(tokenizer().span_tokenize(text)) # list of positions (start,end)
sep = ' ' # word separator; may be language-dependent
lastpos = 0 # lastpos position
for i, w in enumerate(tokens):
    if len(w) >= 3: # ignore less than 3 chars
        w3 = sep.join(tokens[i:i+3])
        if tokens[i+1:i+2] == "-": # check if compound words
            w3 = ''.join(tokens[i:i+3])
        w2 = sep.join(tokens[i:i+2])
        w1 = w
        w3 = w3.title() if w3.isupper() else w3 # NEW YORK CITY => New York City
        w2 = w2.title() if w2.isupper() else w2
        w1 = w1.title() if w1.isupper() else w1
        comp = ['', w1, w2, w3]
        if i+2 < len(tokens) and comp[3] in labels: # 3 words
            label = w3
            start = pos[i][0]
            end = pos[i+2][1]
        elif i+1 < len(tokens) and comp[2] in labels: # 2 words
            label = w2
            start = pos[i][0]
            end = pos[i+1][1]
        elif comp[1] in labels: # 1 word
            label = w1
            start = pos[i][0]
            end = pos[i][1]
        else:
            continue
        if start < lastpos: # skip already processed words
            continue
        lastpos = end
        uri = up(str(labels[label]))
        print('{0}\t{1}\t{2}\t{3}'.format(source, start, end, uri)) # display results
