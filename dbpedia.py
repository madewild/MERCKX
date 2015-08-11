#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tokenize import WordPunctTokenizer as wpt
from jellyfish import levenshtein_distance as ld
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib import unquote_plus as up

import urllib2
import time

import sys
reload(sys)
sys.setdefaultencoding('utf8')
 
def get_labels(uri):
  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
  sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?label
    WHERE { <"""+uri+"""> rdfs:label ?label }
  """)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  labels = set()
  for result in results["results"]["bindings"]:
    labels.add(result["label"]["value"])
  return labels

def get_types(uri):
  sparql = SPARQLWrapper("http://live.dbpedia.org/sparql")
  sparql.setQuery("""
    SELECT DISTINCT ?type
    WHERE { <"""+uri+"""> a ?type }
  """)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  types = set()
  for result in results["results"]["bindings"]:
    types.add(result["type"]["value"])
  return types

def print_uri(ngram,i):
  global s
  global d
  global ind
  global places
  a,z = i
  uri = d[ngram]
  #uri = uri.replace("http://dbpedia.org/resource/", "dbr:")
  if "disambiguation" not in uri and uri in places:
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

places = set()
print "Loading places...",
with open("dbpedia/dbpedia-places.lst") as locs:
  for uri in locs:
    places.add(uri.strip())
print len(places),"locations"

#p = open("5g/fr.txt").read()
p = open("gsc/corr/gsc3_uniline.new.txt").read()
p = p.decode('utf8')
print "Text length:",len(p),"characters"
s = wpt().tokenize(p)
ind = list(wpt().span_tokenize(p))
for i,w in enumerate(s):
  if len(w)>2:
    #w = w.replace('leper','Ieper')
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
