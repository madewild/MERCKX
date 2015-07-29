#!/usr/bin/env python
# coding: utf-8

import urllib,urllib2, json

def coord(place):
  base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
  loc = unicode(place).encode('utf-8')
  url = base_url+loc
  text = urllib2.urlopen(url).read()
  js = json.loads(text)
  res = js["results"]
  if len(res)==1:
    n = 0
  else:
    for i,r in enumerate(res):
      acs = r["address_components"]
      for ac in acs:
        if len(ac["short_name"])==2:
          country = ac["short_name"]
      if country == 'BE':
        n = i
  lat = res[n]["geometry"]["location"]["lat"]
  lng = res[n]["geometry"]["location"]["lng"]
  return lat,lng

f = open("places20.txt").readlines()
f = [l.strip() for l in f]
for l in f:
  p,c = l.split("\t")
  lat,lng = coord(p)
  print [lat,lng,p,int(c)],','
