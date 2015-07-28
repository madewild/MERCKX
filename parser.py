#!/usr/bin/env python
# coding: utf-8

########################
##### YPRES PARSER #####
########################

import re, codecs, os, sys, getopt
import urllib,urllib2
import json
from bs4 import BeautifulSoup as bs
from collections import defaultdict
from jellyfish import levenshtein_distance as ld
from nltk.tokenize import wordpunct_tokenize

#############
# FUNCTIONS #
#############

def get_files(folder):
  listbase = "corpus/"+folder+"/"
  listing = os.listdir(listbase)
  return (listbase,listing)

def get_titles(listbase,listing):
  titles = defaultdict(lambda:[0,set()])
  for f in sorted(listing):
    if len(f)==24:
      ff = listbase+f
      text = open(ff).read()
      soup = bs(text,"xml")
      try:
        title = soup.clip.meta.title.contents[0]
        titles[title][0]+=1
        titles[title][1].add(f)
      except IndexError:
        print "File",f,"has no title"
  return titles

def get_texts(listbase,listing):
  texts = {}
  for f in sorted(listing):
    if len(f) in [23,24]:
      ff = listbase+f
      xml = open(ff).read()
      soup = bs(xml,"xml")
      try:
        body = soup.clip.content.body.find_all("p")
        text = " ".join([par.string for par in body])
        texts[f] = text
      except IndexError:
        print "File",f,"has no body"
  return texts

def get_entities(texts):
  entities = defaultdict(lambda:[0,set()])
  for filename,text in texts.items():
    tokens = wordpunct_tokenize(text)
    for token in tokens:
      if len(token)>4 and token[0].isupper():
        entities[token.capitalize()][0]+=1
        entities[token.capitalize()][1].add(filename)
  return entities

def get_clusters(dic,prec):
  clusters = defaultdict(lambda:[0,0,[]])
  l =  sorted(dic, key=dic.get, reverse=True)[:len(dic)/5]
  for i,e1 in enumerate(l):
    docs = dic[e1][1]
    clusters[e1][0]+=dic[e1][0]
    for e2 in l[i+1:]:
      if e1!=e2 and e1[0]==e2[0] and ld(e1,e2) < prec:
        clusters[e1][0]+=dic[e2][0]
        docs = docs|dic[e2][1]
        clusters[e1][2].append(e2)
        l.remove(e2)
    clusters[e1][1]+=len(docs)
  return clusters

def print_clusters(clusters,dic):
  for c in sorted(clusters, key=clusters.get, reverse=True)[:25]:
    print c
    abstract = get_abstract(c)
    if abstract:
      print abstract
    doc = "articles"
    if clusters[c][1]==1:
      doc = "article"
    print "Cluster size:",len(clusters[c][2])+1
    print clusters[c][0],"mentions from",clusters[c][1],doc
    print "\t",dic[c][0],c
    for match in clusters[c][2]:
      print "\t",dic[match][0],match
    nb = int(eurolib(c))
    if nb==1:
      print "One more result at the European Library"
    elif nb>0:
      print nb,"more results at the European Library"
    print

def eurolib(concept):
  base_url = "http://data.theeuropeanlibrary.org/opensearch/json?"
  param = {}
  param["apikey"] = "4trbi621oika4hd6nqnscr9vcq"
  topic = unicode(concept).encode("utf-8")
  param["query"] = "advanced((SUBJECT,"+topic+"))"
  url = base_url + urllib.urlencode(param)
  text = urllib2.urlopen(url).read()
  json_code = json.loads(text)
  return json_code["NoOfResults"]

def dbpedia(concept):
  base_url = "http://dbpedia.org/data/"
  topic = unicode(concept).encode("utf-8")
  url = base_url+topic+".json"
  text = urllib2.urlopen(url).read()
  try:
    json_code = json.loads(text)
    res = "http://dbpedia.org/resource/"+topic
  except ValueError:
    return {}
  try:
    code = json_code[res]
  except KeyError:
    code = {}
  return code

def get_abstract(concept):
  code = dbpedia(concept)
  onto_abs = "http://dbpedia.org/ontology/abstract"
  try:
    for a in code[onto_abs]:
      if a["lang"]=="en":
         abstract = a["value"]
      elif a["lang"]=="nl":
         abstract = a["value"]
      elif a["lang"]=="fr":
         abstract = a["value"]
    try:
      return re.findall(r"^.+?\.",abstract)[0]
    except UnboundLocalError:
      return False
  except KeyError:
    return False

def texts_by_year(texts):
  yearlist = defaultdict(lambda:[])
  for filename,text in texts.items():
    year = filename[4:8]
    yearlist[year].append(text)
  return yearlist

def get_words(texts):
  words = defaultdict(lambda:0)
  for text in texts:
    tokens = wordpunct_tokenize(text)
    for token in tokens:
      if token.isalpha() and len(token)>3:
        words[token]+=1
  return words

########
# MAIN #
########

def main(argv):
  folder = argv[-1]
  listbase,listing = get_files(folder)
  try:
    opts, args = getopt.getopt(argv,"tew")
  except getopt.GetoptError:
    print "parse.py -t OR -e FOLDER"
    sys.exit(2)
  for opt, arg in opts:
    if opt == "-t":
      titles = get_titles(listbase,listing)
      clusters = get_clusters(titles,4)
      print_clusters(clusters,titles)
    elif opt == "-e":
      texts = get_texts(listbase,listing)
      entities = get_entities(texts)
      clusters = get_clusters(entities,2)
      print_clusters(clusters,entities)
    elif opt == "-w":
      texts = get_texts(listbase,listing)
      freq = get_words(texts.values())
      yearlist = texts_by_year(texts)
      for year in sorted(yearlist):
        print year
        words = get_words(yearlist[year])
        for w in words:
          tf = words[w]
          idf = freq[w]
          x = 1.0*tf/idf
          if idf>10 and x > .7:
            print w,x

if __name__ == "__main__":
    main(sys.argv[1:])
