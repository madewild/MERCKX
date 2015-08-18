#!/usr/bin/env python
# coding: utf-8

########################
##### YPRES PARSER #####
########################

import re, codecs, os,urllib2
from urllib import quote
from xml2dict import XML2Dict
from json import loads
xml = XML2Dict()

#############
# FUNCTIONS #
#############
listing = os.listdir('./ANN/')
for f in sorted(listing):
  if len(f)==24:
    ff = 'ANN/'+f
    tree = xml.parse(ff)
    print "L'article",f,"parle de",
    for par in tree.clip.content.body.p:
      text = codecs.encode(par.value,'utf-8')
      text = re.sub("/","-",text)
      url = 'http://spotlight.dbpedia.org/rest/annotate?text=' + quote(text)
      req = urllib2.Request(url,None,{"Accept":"application/json"})
      #req = urllib2.Request(url,None,{"Accept":"text/xml"})
      resp = urllib2.urlopen(req)
      html = resp.read()
      json = loads(html)
      #print json
      if "Resources" in json:
        for ne in json["Resources"]:
          if float(ne["@percentageOfSecondRank"]) > 0.5:
            print ne["@URI"]+',',
