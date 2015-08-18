#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")

gsc = open("gsc3_uniline.new.txt").read()
gsc = gsc.decode("utf-8")
loc = open("gsc_loc_all.new.txt").readlines()
locs = [l.strip().split("\t") for l in loc]
for l in locs:
  a,z,e = l[:3]
  e = e.decode("utf-8")
  r = gsc[int(a):int(z)]
  if r!=e:
    print a,z,e,r
