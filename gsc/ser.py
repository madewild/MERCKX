#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import sys

x,meth,doc1,doc2 = sys.argv

c = 0
s = 0
d = 0
i = 0

gold = open(doc1).readlines()
guess = open(doc2).readlines()

if meth == "sam":
  n = len(gold)
  for l in gold:
    array = l.split("\t")
    f,a,z,e = array
    for l2 in guess:
      array2 = l2.split("\t")
      ff,aa,zz,ee = array2
      if a==aa and z==zz:
        if e==ee:
          c+=1
        else:
          s+=1
    if l not in guess:
      d+=1
  for l in guess:
    if l not in gold:
      i+=1
elif meth == "ent":
  sgold = set()
  sguess = set()
  for l in gold:
    array = l.split("\t")
    e = array[-1].strip()
    sgold.add(e)
  n = len(sgold)
  for l in guess:
    array = l.split("\t")
    e = array[-1].strip()
    sguess.add(e)
  for e in sgold:
    if e in sguess:
      c+=1
    else:
      d+=1
  for l in sguess:
    if l not in sgold:
      i+=1
else:
  print "Wrong method..."

ser = 1.0*(s+d+i)/n

print "n=",n," c=",c," s=",s," d=",d," i=",i
print "ser=",round(ser,3)
