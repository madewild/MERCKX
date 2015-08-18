#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf8")

raw = open("raw-gold.mapped").readlines()
corr = open("corr-gold.mapped", "w")

loc = open("gsc_loc_all.new.txt").readlines()
locs = [l.strip().split("\t") for l in loc]
for i,l in enumerate(raw):
  c,a,z,e = l.split("\t")
  aa = locs[i][0]
  zz = locs[i][1]
  corr.write(c+"\t"+aa+"\t"+zz+"\t"+e)
corr.close()
