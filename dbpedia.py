#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tokenize import WordPunctTokenizer as wpt
from SPARQLWrapper import SPARQLWrapper, JSON

import sys
reload(sys)
sys.setdefaultencoding('utf8')
 
def get_labels(uri):
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
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
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
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
  a,z = i
  l = len(ngram.split())
  uri = d[ngram]
  types = get_types(uri)
  place = "http://dbpedia.org/ontology/Place"
  sep = "\t"
  if len(ngram)<7:
    sep = "\t\t"
  if "disambiguation" not in uri and place in types:
    #labels = get_labels(uri)
    #print ngram,sep,a,"\t",z,"\t",uri
    print "gsc3.txt\t"+str(a)+"\t"+str(z)+"\t"+uri[28:]
    #print "(also known as",", ".join(labels-set([ngram]))+")"
  for word in ngram.split()[1:]:
    s.remove(word)
    del ind[0]

f = open("dbpedia/labels_nl.nt").readlines()+open("dbpedia/labels_fr.nt").readlines()
print "Processing",len(f),"labels..."
d = dict()
for l in f:
  lok = l.decode("unicode_escape").strip()
  t = lok.split('> "')
  uri = t[0][1:]
  lab = t[1][:-6]
  d[lab]=uri
#p = open("tests/messager.txt").read()
p = open("gsc/gsc3_uniline.txt").read()
#p = "Paris ou Bruxelles?"
p = p.decode('utf-8')
print "Text length:",len(p),"characters"
s = wpt().tokenize(p)
ind = list(wpt().span_tokenize(p))
for i,w in enumerate(s):
  if len(w)>2:
    n3 = " ".join(s[i:i+3])
    n2 = " ".join(s[i:i+2])
    if n3 in d:
      print_uri(n3,a,z)
    elif n2 in d:
      i1 = ind[i]
      i2 = ind[i+1]
      ii = (i1[0],i2[1])
      print_uri(n2,ii)
    elif w in d:
      print_uri(w,ind[i])
