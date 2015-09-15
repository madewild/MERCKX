import re, codecs, os, sys, getopt
#import urllib,urllib2
#import json
from bs4 import BeautifulSoup as bs
from collections import defaultdict
#from jellyfish import levenshtein_distance as ld
#from nltk.tokenize import wordpunct_tokenize
import langid
langid.set_languages(['en','nl','fr'])

def get_files(folder):
  listbase = 'corpus/'+folder+"/"
  listall = os.listdir(listbase)
  listing = [f for f in listall if len(f) in [22,23,24]]
  return (listbase,listing)

folders = os.listdir('corpus/')
#folders = []

#output = codecs.open("output.txt",'a',encoding='utf-8')

#gsc = codecs.open("gsc2.txt").readlines()
#gs = [l.split("\t") for l in gsc]

for folder in sorted(['TYT']):
  #dic = defaultdict(lambda:0)
  listbase,listing = get_files(folder)
  for f in sorted(listing):
    ff = listbase+f
    text = open(ff).read()
    soup = bs(text,"xml")
    try:
      #lang = soup.clip.meta.language.contents[0]
      #first = soup.clip.content.body.p.contents[0]
      body = soup.clip.content.body.find_all('p')
      if body:
        text = " ".join([par.string for par in body if par.string])
        guess1 = langid.classify(text)[0]
        #print f,guess
        #output.write(f+'\t'+lang+'\t'+guess[0]+'\n')
      if True:
        try:
          title = soup.clip.meta.title.contents[0]
          guess2 = langid.classify(title)[0]
        except (IndexError, AttributeError,TypeError) as e:
          #dic['?2']+=1
          print f,e
      if guess1 != guess2:
        print f,guess1,guess2
    except (IndexError, AttributeError,TypeError) as e:
      dic['?1']+=1
      print f,e
  #print folder,dic
