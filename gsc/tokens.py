#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tokenize import WordPunctTokenizer as wpt

import sys
reload(sys)
sys.setdefaultencoding('utf8')

gsc = open("gsc3.txt").readlines()
en = gsc[:2]
fr = gsc[2:51]
nl = gsc[51:]
for x in [en,fr,nl]:
  c = 0
  for l in x:
    l = l.strip().decode("utf-8")
    w = wpt().tokenize(l)
    n = len(w)
    c+=n
  print c
