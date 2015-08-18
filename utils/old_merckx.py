#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################
##### MERCKX #####
##################

from nltk.tokenize import WordPunctTokenizer as wpt
from urllib import unquote_plus as up
import urllib2

# from jellyfish import levenshtein_distance as ld
# to add support for clustering

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def print_uri(ngram,i):
  global s
  global d
  global ind
  a,z = i
  uri = d[ngram]
  print "gsc3.txt\t"+str(a)+"\t"+str(z)+"\t"+up(str(uri[4:]))
  for word in ngram.split()[1:]:
    s.remove(word)
    del ind[0]

d = dict()
print "Building label dictionary...",
filename = "dbpedia/dbpedia-labels.lst"
with open(filename) as f:
  for l in f:
    lok = l.decode("utf8").strip()
    t = lok.split('\t')
    lab = t[0]
    uri = t[1]
    d[lab] = uri
print len(d),"labels"

#p = open("gsc/corr/gsc3_uniline.new.txt").read()
p = open("perelman_uniline.txt").read()
p = p.decode('utf8')
print "Text length:",len(p),"characters"
s = wpt().tokenize(p)
ind = list(wpt().span_tokenize(p))
for i,w in enumerate(s):
  if len(w)>2:
    if w.isupper():
      w = w.capitalize()
    if s[i+1]=="-": # if compound
      n3 = "".join(s[i:i+3])
    else:
      n3 = " ".join(s[i:i+3])
    n2 = " ".join(s[i:i+2])
    if n3 in d:
      i1 = ind[i]
      i3 = ind[i+2]
      ii = (i1[0],i3[1])
      print_uri(n3,ii)
    elif n2 in d:
      i1 = ind[i]
      i2 = ind[i+1]
      ii = (i1[0],i2[1])
      print_uri(n2,ii)
    elif w in d:
      print_uri(w,ind[i])
